import React from 'react';
import { useEmailStore } from '../store/useEmailStore';
import '../styles/Message.css';

const Message = () => {
  const message = useEmailStore((state) => state.message);
  const messageType = useEmailStore((state) => state.messageType);

  if (!message) return null;

  return (
    <div className={`message message-${messageType}`}>
      {message}
    </div>
  );
};

export default Message;
