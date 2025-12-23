export const validateEmail = (email) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

export const validatePrompt = (prompt, minLength = 10) => {
  return prompt.trim().length >= minLength;
};
