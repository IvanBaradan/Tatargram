import React from 'react';

const TelegramIcon = ({ style = {}, className = '' }) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      style={{ width: '24px', height: '24px', ...style }}
      className={className}
    >
      <path
        fill="#0088cc"
        d="M12 0c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.447 1.394c-.14.141-.259.259-.374.261l.213-3.053 5.56-5.022c.24-.213-.054-.334-.373-.121l-6.869 4.326-2.96-.924c-.64-.203-.658-.64.136-.954l11.566-4.458c.538-.196 1.006.128.832.941z"
      />
    </svg>
  );
};

export default TelegramIcon;