import { sum3, infiniteSum, add, curry } from './curry.js';

console.log('🥋 --- TESTING CURRYING DRILLS ---');

// Test Level 1: sum3
try {
  const r1 = sum3(1)(2)(3);
  console.log(`Level 1 (sum3(1)(2)(3)): ${r1 === 6 ? '✅ PASS' : '❌ FAIL (got ' + r1 + ')'}`);
} catch (e) {
  console.log(`Level 1 (sum3): ⏳ NOT IMPLEMENTED YET (${e.message})`);
}

// Test Level 2: infiniteSum
try {
  const r2a = infiniteSum(1)(2)(3)();
  const r2b = infiniteSum(5)(10)(2)(1)();
  const r2c = infiniteSum();
  const pass2 = r2a === 6 && r2b === 18 && r2c === 0;
  console.log(`Level 2 (infiniteSum): ${pass2 ? '✅ PASS' : '❌ FAIL'}`);
} catch (e) {
  console.log(`Level 2 (infiniteSum): ⏳ NOT IMPLEMENTED YET (${e.message})`);
}

// Test Level 3: add (coercion)
try {
  const r3 = add(1)(2)(3);
  const pass3 = (r3 == 6) && (r3 + 4 === 10);
  console.log(`Level 3 (add with valueOf): ${pass3 ? '✅ PASS' : '❌ FAIL'}`);
} catch (e) {
  console.log(`Level 3 (add): ⏳ NOT IMPLEMENTED YET (${e.message})`);
}

// Test Level 4: universal curry
try {
  const join = (a, b, c) => `${a}_${b}_${c}`;
  const curriedJoin = curry(join);
  const pass4 =
    curriedJoin(1)(2)(3) === '1_2_3' &&
    curriedJoin(1, 2)(3) === '1_2_3' &&
    curriedJoin(1)(2, 3) === '1_2_3' &&
    curriedJoin(1, 2, 3) === '1_2_3';
  console.log(`Level 4 (universal curry): ${pass4 ? '✅ PASS' : '❌ FAIL'}`);
} catch (e) {
  console.log(`Level 4 (curry): ⏳ NOT IMPLEMENTED YET (${e.message})`);
}
