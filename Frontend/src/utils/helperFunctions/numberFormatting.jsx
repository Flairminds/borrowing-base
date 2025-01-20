export const formatNumber = (number) => {
  let check = false;
  if (number < 0) check = true;
  if (check == true) {
    number = -(number);
      if (number >= 1e9) {
        return '-' + (number / 1e9).toFixed(2) + 'B';
      } else if (number >= 1e6) {
        return '-' + (number / 1e6).toFixed(2) + 'M';
      } else if (number >= 1e3) {
        return '-' + (number / 1e3).toFixed(2) + 'K';
      } else {
        return '-' + number.toLocaleString();
      }

  } else {
    if (number >= 1e9) {
      return (number / 1e9).toFixed(2) + 'B';
    } else if (number >= 1e6) {
      return (number / 1e6).toFixed(2) + 'M';
    } else if (number >= 1e3) {
      return (number / 1e3).toFixed(2) + 'K';
    } else {
      return number.toLocaleString();
    }
  }
  };