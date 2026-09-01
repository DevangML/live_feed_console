// Partial Application

function sum(a) {
  return function (b, c) {
    return a + b + c;
  };
}

