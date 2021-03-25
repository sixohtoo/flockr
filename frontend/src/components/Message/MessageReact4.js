import React from 'react';
import axios from 'axios';

import {
  Badge,
  IconButton,
} from '@material-ui/core';

import StarIcon from '@material-ui/icons/Star';
import StarBorderOutlinedIcon from '@material-ui/icons/StarBorderOutlined';
import yellow from "@material-ui/core/colors/yellow";

import AuthContext from '../../AuthContext';
import {StepContext} from '../Channel/ChannelMessages';

function MessageReact4({
  message_id,
  reacts = [] /* [{ react_id, u_ids }] */,
}) {

  const token = React.useContext(AuthContext);
  let step = React.useContext(StepContext);
  step = step ? step : () => {}; // sanity check

  const messageReact4 = (is_reacted) => {
    if (is_reacted) {
      axios.post(`/message/unreact`, {
        token,
        message_id: Number.parseInt(message_id),
        react_id: 4 /* FIXME */,
      })
      .then(() => {
        step();
      });
    } else {
      axios.post(`/message/react`, {
        token,
        message_id: Number.parseInt(message_id),
        react_id: 4 /* FIXME */,
      })
      .then(() => {
        step();
      });
    }
  };

  let starCount = 0;
  let is_reacted = false;
  const starIndex = reacts.findIndex((react) => react.react_id === 4);
  if (starIndex !== -1) {
    starCount = reacts[starIndex].u_ids.length;
    is_reacted = reacts[starIndex].is_this_user_reacted;
  }

  return (
    <Badge
      anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      badgeContent={starCount}
      color="secondary"
    >
      <IconButton
        onClick={() => messageReact4(is_reacted)}
        style={{ margin: 1 }}
        size="small"
        edge="end"
        aria-label="delete"
      >
        {is_reacted ? (
          <StarIcon fontSize="small" style={{color: yellow[500]}}/>
          ) : (
          <StarBorderOutlinedIcon fontSize="small" />
        )}
      </IconButton>
    </Badge>
  );
}

export default MessageReact4;
