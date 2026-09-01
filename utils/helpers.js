export function capitalize(s) {
  if (!(typeof s === string)) {
    throw TypeError(`${s} is of invalid type`);
  }

  return s.charAt(0).toUpperCase() + s.slice(1);
}
