// Currying in javascript
// Example f(a,b) into f(a)(b)

function f(a) {
  return function (b) {
    console.log(`${a} ${b}`);
  };
}

console.log(f(5)(6));
