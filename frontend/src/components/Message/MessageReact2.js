import React from 'react';
import axios from 'axios';

import {
  Badge,
  IconButton,
} from '@material-ui/core';

import ThumbDownIcon from '@material-ui/icons/ThumbDown';
import ThumbDownOutlinedIcon from '@material-ui/icons/ThumbDownOutlined';

import AuthContext from '../../AuthContext';
import {StepContext} from '../Channel/ChannelMessages';

function MessageReact2({
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
        react_id: 2 /* FIXME */,
      })
      .then(() => {
        step();
      });
    } else {
      axios.post(`/message/react`, {
        token,
        message_id: Number.parseInt(message_id),
        react_id: 2 /* FIXME */,
      })
      .then(() => {
        step();
      });
    }
  };

  let thumbDownCount = 0;
  let is_reacted = false;
  const thumbDownIndex = reacts.findIndex((react) => react.react_id === 2);
  if (thumbDownIndex !== -1) {
    thumbDownCount = reacts[thumbDownIndex].u_ids.length;
    is_reacted = reacts[thumbDownIndex].is_this_user_reacted;
  }

  return (
    <Badge
      anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      badgeContent={thumbDownCount}
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
          <ThumbDownIcon fontSize="small" />
          ) : (
          <ThumbDownOutlinedIcon fontSize="small" />
        )}
      </IconButton>
    </Badge>
  );
}

export default MessageReact2;
