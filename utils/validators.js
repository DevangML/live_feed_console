export const VALIDATORS = {
  string: {
    checkType: (v) => typeof v === 'string',
    isEmpty: (v) => v === '',
  },
  number: {
    checkType: (v) => typeof v === 'number' && !Number.isNaN(v),
    isEmpty: (v) => false, // Numbers do not have empty in the same sense
  },
  array: {
    checkType: (v) => Array.isArray(v),
    isEmpty: (v) => Array.isArray(v) && v.length === 0,
  },
};
