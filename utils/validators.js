export const VALIDATORS = {
  string: {
    checkType: (v) => typeof v === 'string',
    isEmpty: (v) => v.trim() === '',
  },
  number: {
    checkType: (v) => typeof v === 'number' && !Number.isNaN(v),
    isEmpty: (v) => false, // Numbers do not have empty in the same sense
  },
  array: {
    checkType: (v) => Array.isArray(v),
    isEmpty: (v) =>
      Array.isArray(v) === true &&
      (v.length === 0 ||
        v.some((e) => typeof e === 'string' && e.trim() === '')),
  },
};
