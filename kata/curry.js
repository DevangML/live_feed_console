/**
 * ============================================================================
 * 🥋 THE CURRYING CRUCIBLE: FROM METTL MCQS TO MACHINE CODING (3 YOE)
 * ============================================================================
 *
 * Currying is the technique of converting a function that takes multiple arguments:
 *   f(a, b, c) ──▶ f(a)(b)(c)
 *
 * In interview assessments (Mettl OA, Accenture Advanced JS, FAANG Screenings),
 * currying tests 4 core pillars:
 * 1. Closure lexical scope retention
 * 2. Function Arity (`fn.length`) mechanics & traps
 * 3. Variadic vs Fixed-Arity argument accumulation
 * 4. ValueOf / ToString type coercion tricks
 *
 * Below are the 5 canonical interview problems ranging from Level 1 to Level 5.
 */

// ============================================================================
// 🥊 LEVEL 1: THE WARMUP — Fixed 3-Arity Sum
// ============================================================================
/**
 * PROBLEM 1: Write a function `sum3` such that:
 *   sum3(1)(2)(3) === 6
 *
 * Target concept: Nested closure returns.
 */
function sum3(a) {
  return function (b) {
    return function (c) {
      return a + b + c;
    };
  };
}
console.log(sum3(1)(2)(3));

// ============================================================================
// 🥊 LEVEL 2: THE CLASSIC OA DRILL — Infinite Currying with Empty Invocation
// ============================================================================
/**
 * PROBLEM 2 (Very Common in Mettl/TCS/Accenture):
 * Write a function `infiniteSum` that accumulates numbers indefinitely until
 * called with NO arguments `()`:
 *
 * Examples:
 *   infiniteSum(1)(2)(3)() === 6
 *   infiniteSum(5)(10)(2)(1)() === 18
 *   infiniteSum() === 0
 *
 * Target concept: Checking `args.length === 0` to terminate recursion.
 */
function infiniteSum(a) {
  if (a === undefined) {
    return 0;
  }

  return function next(b) {
    // If b is provided, keep accumulating and return the next function recursively
    if (b !== undefined) {
      return infiniteSum(a + b);
    }

    // If b is undefined
    return a;
  };
}

const result = infiniteSum(1)(2)(3)(4)();

console.log(result);

// ============================================================================
// 🥊 LEVEL 3: THE COERCION TRAP — Infinite Currying with Type Conversion
// ============================================================================
/**
 * PROBLEM 3 (Advanced Mettl MCQ / Tricky Machine Coding):
 * Write a function `add` such that it can be chained indefinitely WITHOUT
 * needing an empty `()`, but evaluates to the sum in numeric/string contexts:
 *
 * Examples:
 *   add(1)(2)(3) == 6        (Evaluates to true with loose equality!)
 *   add(1)(2)(3) + 4 === 10
 *   console.log(add(1)(2))   // prints 3 or [Function] with valueOf = 3
 *
 * Target concept: Overriding `Function.prototype.valueOf` / `Symbol.toPrimitive`.
 */
function infiniteSum2(a) {
  if (a === undefined) {
    return 0;
  }

  const next = function (b) {
    if (b !== undefined) {
      return infiniteSum2(a + b);
    }

    return a;
  };

  next.valueOf = function () {
    return a;
  };

  return next;
}

const result2 = infiniteSum2(1)(2) + 40 === 43;
console.log(result2);

// ============================================================================
// 🥊 LEVEL 4: THE GENERAL PURPOSE `curry(fn)` IMPLEMENTATION
// ============================================================================
/**
 * PROBLEM 4 (Standard FAANG / Senior Machine Coding):
 * Write the universal `curry` function that transforms ANY normal function `fn`
 * into a curried version supporting arbitrary partial applications:
 *
 * Examples:
 *   const join = (a, b, c) => `${a}_${b}_${c}`;
 *   const curriedJoin = curry(join);
 *
 *   curriedJoin(1)(2)(3)    === "1_2_3"
 *   curriedJoin(1, 2)(3)    === "1_2_3"
 *   curriedJoin(1)(2, 3)    === "1_2_3"
 *   curriedJoin(1, 2, 3)    === "1_2_3"
 *
 * Target concept: `fn.length` arity check + `args.concat(nextArgs)`.
 */
function curry(fn) {
  return function curried(...args) {
    if (args.length >= fn.length) {
      return fn(...args);
    }
    return function (...next) {
      return curried(...args, ...next);
    };
  };
}

// ============================================================================
// 🥊 LEVEL 5: THE PLACEHOLDER CURRY (Lodash `_` Style)
// ============================================================================
/**
 * PROBLEM 5 (Staff Level Edge-Case):
 * Extend `curry` to support placeholders `curry.placeholder` (like `_` in Ramda/Lodash),
 * allowing arguments to be supplied out-of-order:
 *
 * Examples:
 *   const _ = curryWithPlaceholder.placeholder;
 *   const subtract = (a, b, c) => a - b - c;
 *   const curriedSub = curryWithPlaceholder(subtract);
 *
 *   curriedSub(_, 2)(5, 1) === (5 - 2 - 1) === 2
 *   curriedSub(_, _, 1)(5)(2) === (5 - 2 - 1) === 2
 */
function curryWithPlaceholder(fn) {
  return;
}
curryWithPlaceholder.placeholder = Symbol('curry_placeholder');

// ============================================================================
// 🧠 METTL OA MCQ PRACTICE BANK (Predict the Output)
// ============================================================================
/**
 * ❓ MCQ 1: What is the output?
 * ----------------------------
 * function f1(a, b = 2, c) {}
 * console.log(f1.length);
 *
 * A) 3
 * B) 1
 * C) 2
 * D) undefined
 *
 * 💡 Rule to know: `fn.length` stops counting parameters the moment it hits
 * the FIRST parameter with a default value (`b = 2`). So `f1.length` is 1!
 *
 * ----------------------------
 * ❓ MCQ 2: What is the output?
 * ----------------------------
 * function f2(a, ...rest) {}
 * console.log(f2.length);
 *
 * A) 1
 * B) 2
 * C) Infinity
 * D) 0
 *
 * 💡 Rule to know: Rest parameters (`...rest`) are NOT counted in `fn.length`.
 * So `f2.length` is 1!
 *
 * ----------------------------
 * ❓ MCQ 3: What is the output?
 * ----------------------------
 * const multiply = (a) => (b) => a * b;
 * const double = multiply(2);
 * const triple = multiply(3);
 * console.log(double(triple(4)));
 *
 * A) 24
 * B) 14
 * C) NaN
 * D) TypeError
 *
 * 💡 Explanation: `triple(4)` produces `3 * 4 = 12`. Then `double(12)` produces `2 * 12 = 24`.
 */

export {
  sum3,
  infiniteSum,
  infiniteSum2 as add,
  curry,
  curryWithPlaceholder
};
