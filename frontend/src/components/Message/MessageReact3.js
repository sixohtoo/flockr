import React from 'react';
import axios from 'axios';

import {
  Badge,
  IconButton,
} from '@material-ui/core';

import FavoriteIcon from '@material-ui/icons/Favorite';
import FavoriteBorderIcon from '@material-ui/icons/FavoriteBorder';
import red from "@material-ui/core/colors/red";

import AuthContext from '../../AuthContext';
import {StepContext} from '../Channel/ChannelMessages';

function MessageReact3({
  message_id,
  reacts = [] /* [{ react_id, u_ids }] */,
}) {

  const token = React.useContext(AuthContext);
  let step = React.useContext(StepContext);
  step = step ? step : () => {}; // sanity check

  const messageReact = (is_reacted) => {
    if (is_reacted) {
      axios.post(`/message/unreact`, {
        token,
        message_id: Number.parseInt(message_id),
        react_id: 3 /* FIXME */,
      })
      .then(() => {
        step();
      });
    } else {
      axios.post(`/message/react`, {
        token,
        message_id: Number.parseInt(message_id),
        react_id: 3 /* FIXME */,
      })
      .then(() => {
        step();
      });
    }
  };

  let favouriteCount = 0;
  let is_reacted = false;
  const favouriteIndex = reacts.findIndex((react) => react.react_id === 3);
  if (favouriteIndex !== -1) {
    favouriteCount = reacts[favouriteIndex].u_ids.length;
    is_reacted = reacts[favouriteIndex].is_this_user_reacted;
  }

  return (
    <Badge
      anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      badgeContent={favouriteCount}
      color="secondary"
    >
      <IconButton
        onClick={() => messageReact(is_reacted)}
        style={{ margin: 1 }}
        size="small"
        edge="end"
        aria-label="delete"
      >
        {is_reacted ? (
          <FavoriteIcon fontSize="small" style={{color: red[500]}} />
          ) : (
          <FavoriteBorderIcon fontSize="small" />
        )}
      </IconButton>
    </Badge>
  );
}

export default MessageReact3;
