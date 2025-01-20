import { toast } from 'react-toastify';

export const showToast = (type, message, duration = 1500) => {
  const options = { autoClose: duration, closeOnClick: true, pauseOnHover: true };

  if (toast[type]) {
    toast[type](message, options);
  } else {
    toast(message, options);
  }
};
