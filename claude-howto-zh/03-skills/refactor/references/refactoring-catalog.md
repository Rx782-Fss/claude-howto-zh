# 重构手法目录

基于 Martin Fowler《重构(Refactoring)》(第2版)的精选重构手法目录。每种重构都包含动机、分步操作说明和示例。

> "重构是由其操作机制定义的----即执行变更所遵循的精确步骤序列。" -- Martin Fowler

---

## 如何使用本目录

1. **识别异味** ---- 使用代码异味参考来定位问题
2. **找到匹配的重构** ---- 在本目录中查找对应的手法
3. **遵循操作机制** ---- 逐步执行
4. **每步测试** ---- 确保行为保持不变

**黄金法则**:如果任何一步耗时超过 10 分钟,请将其拆分为更小的步骤。

---

## 最常用的重构手法

### 提取方法(Extract Method)

**适用场景**:长方法、重复代码、需要为某个概念命名

**动机**:将一段代码转化为一个方法,用名称解释其用途

**操作步骤**:
1. 创建一个新方法,以其功能命名(而非实现方式)
2. 将代码片段复制到新方法中
3. 扫描片段中使用的局部变量
4. 将局部变量作为参数传递(或在方法内声明)
5. 适当处理返回值
6. 用对新方法的调用替换原始代码片段
7. 测试

**重构前**:
```javascript
function printOwing(invoice) {
  let outstanding = 0;

  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");

  // 计算欠款金额
  for (const order of invoice.orders) {
    outstanding += order.amount;
  }

  // 打印详情
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}
```

**重构后**:
```javascript
function printOwing(invoice) {
  printBanner();
  const outstanding = calculateOutstanding(invoice);
  printDetails(invoice, outstanding);
}

function printBanner() {
  console.log("***********************");
  console.log("**** Customer Owes ****");
  console.log("***********************");
}

function calculateOutstanding(invoice) {
  return invoice.orders.reduce((sum, order) => sum + order.amount, 0);
}

function printDetails(invoice, outstanding) {
  console.log(`name: ${invoice.customer}`);
  console.log(`amount: ${outstanding}`);
}
```

---

### 内联方法(Inline Method)

**适用场景**:方法体和名字一样清晰、过度委托

**动机**:当方法不增加价值时,移除不必要的间接层

**操作步骤**:
1. 确认该方法不是多态的
2. 找到所有对该方法的调用
3. 用方法体替换每个调用
4. 每次替换后进行测试
5. 移除方法定义

**重构前**:
```javascript
function getRating(driver) {
  return moreThanFiveLateDeliveries(driver) ? 2 : 1;
}

function moreThanFiveLateDeliveries(driver) {
  return driver.numberOfLateDeliveries > 5;
}
```

**重构后**:
```javascript
function getRating(driver) {
  return driver.numberOfLateDeliveries > 5 ? 2 : 1;
}
```

---

### 提取变量(Extract Variable)

**适用场景**:难以理解的复杂表达式

**动机**:给复杂表达式的某一部分命名

**操作步骤**:
1. 确保表达式没有副作用
2. 声明一个不可变变量
3. 将其设为表达式(或部分表达式)的结果
4. 用该变量替换原表达式
5. 测试

**重构前**:
```javascript
return order.quantity * order.itemPrice -
  Math.max(0, order.quantity - 500) * order.itemPrice * 0.05 +
  Math.min(order.quantity * order.itemPrice * 0.1, 100);
```

**重构后**:
```javascript
const basePrice = order.quantity * order.itemPrice;
const quantityDiscount = Math.max(0, order.quantity - 500) * order.itemPrice * 0.05;
const shipping = Math.min(basePrice * 0.1, 100);
return basePrice - quantityDiscount + shipping;
```

---

### 内联变量(Inline Variable)

**适用场景**:变量名没有比表达式传达更多信息

**动机**:移除不必要的间接层

**操作步骤**:
1. 检查等号右边是否有副作用
2. 如果变量不是不可变的,先使其不可变并测试
3. 找到第一个引用处并用表达式替换
4. 测试
5. 对所有引用重复上述步骤
6. 移除声明和赋值
7. 测试

---

### 重命名变量(Rename Variable)

**适用场景**:名称没有清晰地传达目的

**动机**:好的名称对整洁代码至关重要

**操作步骤**:
1. 如果变量被广泛使用,考虑封装
2. 找到所有引用
3. 修改每个引用
4. 测试

**技巧**:
- 使用意图明确的名称
- 避免缩写
- 使用领域术语

```javascript
// 差
const d = 30;
const x = users.filter(u => u.a);

// 好
const daysSinceLastLogin = 30;
const activeUsers = users.filter(user => user.isActive);
```

---

### 修改函数声明(Change Function Declaration)

**适用场景**:函数名未解释目的、参数需要变更

**动机**:好的函数名让代码自文档化

**操作步骤(简单情况)**:
1. 移除不需要的参数
2. 修改名称
3. 添加需要的参数
4. 测试

**操作步骤(迁移模式 -- 用于复杂变更)**:
1. 如需移除参数,确认其未被使用
2. 创建具有期望声明的新函数
3. 让旧函数调用新函数
4. 测试
5. 将调用方改为使用新函数
6. 每次修改后测试
7. 移除旧函数

**重构前**:
```javascript
function circum(radius) {
  return 2 * Math.PI * radius;
}
```

**重构后**:
```javascript
function circumference(radius) {
  return 2 * Math.PI * radius;
}
```

---

### 封装变量(Encapsulate Variable)

**适用场景**:从多个地方直接访问数据

**动机**:为数据操作提供清晰的访问点

**操作步骤**:
1. 创建 getter 和 setter 函数
2. 找到所有引用
3. 用 getter 替换读取
4. 用 setter 替换写入
5. 每次更改后测试
6. 限制变量的可见性

**重构前**:
```javascript
let defaultOwner = { firstName: "Martin", lastName: "Fowler" };

// 在多处使用
spaceship.owner = defaultOwner;
```

**重构后**:
```javascript
let defaultOwnerData = { firstName: "Martin", lastName: "Fowler" };

function defaultOwner() { return defaultOwnerData; }
function setDefaultOwner(arg) { defaultOwnerData = arg; }

spaceship.owner = defaultOwner();
```

---

### 引入参数对象(Introduce Parameter Object)

**适用场景**:多个参数总是成组出现

**动机**:将天然属于一组的数据组织在一起

**操作步骤**:
1. 为成组参数创建新的类/结构体
2. 测试
3. 使用"修改函数声明"添加新对象
4. 测试
5. 对于组中的每个参数,从函数中移除并改用新对象
6. 每次移除后测试

**重构前**:
```javascript
function amountInvoiced(startDate, endDate) { ... }
function amountReceived(startDate, endDate) { ... }
function amountOverdue(startDate, endDate) { ... }
```

**重构后**:
```javascript
class DateRange {
  constructor(start, end) {
    this.start = start;
    this.end = end;
  }
}

function amountInvoiced(dateRange) { ... }
function amountReceived(dateRange) { ... }
function amountOverdue(dateRange) { ... }
```

---

### 将函数组合成类(Combine Functions into Class)

**适用场景**:多个函数操作同一份数据

**动机**:将函数与它们所操作的数据组织在一起

**操作步骤**:
1. 对公共数据应用"封装记录"
2. 将每个函数移入类中
3. 每次移动后测试
4. 用类字段的使用替换数据参数

**重构前**:
```javascript
function base(reading) { ... }
function taxableCharge(reading) { ... }
function calculateBaseCharge(reading) { ... }
```

**重构后**:
```javascript
class Reading {
  constructor(data) { this._data = data; }

  get base() { ... }
  get taxableCharge() { ... }
  get calculateBaseCharge() { ... }
}
```

---

### 拆分阶段(Split Phase)

**适用场景**:代码处理两件不同的事情

**动机**:将代码拆分为有清晰边界的不同阶段

**操作步骤**:
1. 为第二阶段创建第二个函数
2. 测试
3. 在阶段之间引入中间数据结构
4. 测试
5. 将第一阶段提取到自己的函数中
6. 测试

**重构前**:
```javascript
function priceOrder(product, quantity, shippingMethod) {
  const basePrice = product.basePrice * quantity;
  const discount = Math.max(quantity - product.discountThreshold, 0)
    * product.basePrice * product.discountRate;
  const shippingPerCase = (basePrice > shippingMethod.discountThreshold)
    ? shippingMethod.discountedFee : shippingMethod.feePerCase;
  const shippingCost = quantity * shippingPerCase;
  return basePrice - discount + shippingCost;
}
```

**重构后**:
```javascript
function priceOrder(product, quantity, shippingMethod) {
  const priceData = calculatePricingData(product, quantity);
  return applyShipping(priceData, shippingMethod);
}

function calculatePricingData(product, quantity) {
  const basePrice = product.basePrice * quantity;
  const discount = Math.max(quantity - product.discountThreshold, 0)
    * product.basePrice * product.discountRate;
  return { basePrice, quantity, discount };
}

function applyShipping(priceData, shippingMethod) {
  const shippingPerCase = (priceData.basePrice > shippingMethod.discountThreshold)
    ? shippingMethod.discountedFee : shippingMethod.feePerCase;
  const shippingCost = priceData.quantity * shippingPerCase;
  return priceData.basePrice - priceData.discount + shippingCost;
}
```

---

## 搬移特性(Moving Features)

### 搬移方法(Move Method)

**适用场景**:方法使用了另一个类更多的特性

**动机**:将函数放在它最常使用的数据附近

**操作步骤**:
1. 检查方法在其类中使用的所有程序元素
2. 检查方法是否是多态的
3. 将方法复制到目标类
4. 调整以适应新上下文
5. 让原始方法委托给目标方法
6. 测试
7. 考虑移除原始方法

---

### 搬移字段(Move Field)

**适用场景**:字段被另一个类更多地使用

**动机**:让数据与使用它的函数在一起

**操作步骤**:
1. 封装该字段(如果尚未封装)
2. 测试
3. 在目标类中创建字段
4. 更新引用以使用目标字段
5. 测试
6. 移除原始字段

---

### 将语句搬入函数(Move Statements into Function)

**适用场景**:相同的代码总是与一个函数调用一起出现

**动机**:通过将重复代码移入函数来消除重复

**操作步骤**:
1. 如果还没有,先将重复代码提取为函数
2. 将语句移入该函数
3. 测试
4. 如果调用方不再需要独立语句,则移除它们

---

### 将语句搬移到调用方(Move Statements to Callers)

**适用场景**:调用方之间的共同行为存在差异

**动机**:当行为需要不同时,将其从函数中移出

**操作步骤**:
1. 对要移动的代码使用"提取方法"
2. 对原始函数使用"内联方法"
3. 移除现已内联的调用
4. 将提取的代码移到每个调用方
5. 测试

---

## 组织数据(Organizing Data)

### 以对象取代基本类型(Replace Primitive with Object)

**适用场景**:数据项需要比简单值更多的行为

**动机**:将数据与其行为封装在一起

**操作步骤**:
1. 应用"封装变量"
2. 创建简单的值类
3. 修改 setter 以创建新实例
4. 修改 getter 以返回值
5. 测试
6. 为新类添加更丰富的行为

**重构前**:
```javascript
class Order {
  constructor(data) {
    this.priority = data.priority; // 字符串: "high", "rush" 等
  }
}

// 使用方式
if (order.priority === "high" || order.priority === "rush") { ... }
```

**重构后**:
```javascript
class Priority {
  constructor(value) {
    if (!Priority.legalValues().includes(value))
      throw new Error(`Invalid priority: ${value}`);
    this._value = value;
  }

  static legalValues() { return ['low', 'normal', 'high', 'rush']; }
  get value() { return this._value; }

  higherThan(other) {
    return Priority.legalValues().indexOf(this._value) >
           Priority.legalValues().indexOf(other._value);
  }
}

// 使用方式
if (order.priority.higherThan(new Priority("normal"))) { ... }
```

---

### 以查询取代临时变量(Replace Temp with Query)

**适用场景**:临时变量保存了表达式的结果

**动机**:通过将表达式提取为函数使代码更清晰

**操作步骤**:
1. 确认变量只被赋值一次
2. 将赋值右边提取为一个方法
3. 用方法调用替换对临时变量的引用
4. 测试
5. 移除临时变量的声明和赋值

**重构前**:
```javascript
const basePrice = this._quantity * this._itemPrice;
if (basePrice > 1000) {
  return basePrice * 0.95;
} else {
  return basePrice * 0.98;
}
```

**重构后**:
```javascript
get basePrice() {
  return this._quantity * this._itemPrice;
}

// 在方法中使用
if (this.basePrice > 1000) {
  return this.basePrice * 0.95;
} else {
  return this.basePrice * 0.98;
}
```

---

## 简化条件逻辑(Simplifying Conditional Logic)

### 分解条件表达式(Decompose Conditional)

**适用场景**:复杂的条件(if-then-else)语句

**动机**:通过提取条件和动作来明确意图

**操作步骤**:
1. 对条件应用"提取方法"
2. 对 then 分支应用"提取方法"
3. 对 else 分支应用"提取方法"(如果存在)

**重构前**:
```javascript
if (!aDate.isBefore(plan.summerStart) && !aDate.isAfter(plan.summerEnd)) {
  charge = quantity * plan.summerRate;
} else {
  charge = quantity * plan.regularRate + plan.regularServiceCharge;
}
```

**重构后**:
```javascript
if (isSummer(aDate, plan)) {
  charge = summerCharge(quantity, plan);
} else {
  charge = regularCharge(quantity, plan);
}

function isSummer(date, plan) {
  return !date.isBefore(plan.summerStart) && !date.isAfter(plan.summerEnd);
}

function summerCharge(quantity, plan) {
  return quantity * plan.summerRate;
}

function regularCharge(quantity, plan) {
  return quantity * plan.regularRate + plan.regularServiceCharge;
}
```

---

### 合并条件表达式(Consolidate Conditional Expression)

**适用场景**:多个条件产生相同结果

**动机**:明确这些条件是同一个检查

**操作步骤**:
1. 确认条件中没有副作用
2. 使用 `and` 或 `or` 合并条件
3. 考虑对合并后的条件应用"提取方法"

**重构前**:
```javascript
if (employee.seniority < 2) return 0;
if (employee.monthsDisabled > 12) return 0;
if (employee.isPartTime) return 0;
```

**重构后**:
```javascript
if (isNotEligibleForDisability(employee)) return 0;

function isNotEligibleForDisability(employee) {
  return employee.seniority < 2 ||
         employee.monthsDisabled > 12 ||
         employee.isPartTime;
}
```

---

### 以卫语句取代嵌套条件(Replace Nested Conditional with Guard Clauses)

**适用场景**:深层嵌套的条件使流程难以跟随

**动机**:对特殊情况使用卫语句,保持正常流程清晰

**操作步骤**:
1. 找到特殊情况的条件
2. 用提前返回的卫语句替换它们
3. 每次更改后测试

**重构前**:
```javascript
function payAmount(employee) {
  let result;
  if (employee.isSeparated) {
    result = { amount: 0, reasonCode: "SEP" };
  } else {
    if (employee.isRetired) {
      result = { amount: 0, reasonCode: "RET" };
    } else {
      result = calculateNormalPay(employee);
    }
  }
  return result;
}
```

**重构后**:
```javascript
function payAmount(employee) {
  if (employee.isSeparated) return { amount: 0, reasonCode: "SEP" };
  if (employee.isRetired) return { amount: 0, reasonCode: "RET" };
  return calculateNormalPay(employee);
}
```

---

### 以多态取代条件式(Replace Conditional with Polymorphism)

**适用场景**:基于类型的 switch/case、随类型变化的条件逻辑

**动机**:让对象自己处理自己的行为

**操作步骤**:
1. 创建类层级(如果不存在)
2. 使用工厂函数创建对象
3. 将条件逻辑移入超类方法
4. 为每种 case 创建子类方法
5. 移除原始条件

**重构前**:
```javascript
function plumages(birds) {
  return birds.map(b => plumage(b));
}

function plumage(bird) {
  switch (bird.type) {
    case 'EuropeanSwallow':
      return "average";
    case 'AfricanSwallow':
      return (bird.numberOfCoconuts > 2) ? "tired" : "average";
    case 'NorwegianBlueParrot':
      return (bird.voltage > 100) ? "scorched" : "beautiful";
    default:
      return "unknown";
  }
}
```

**重构后**:
```javascript
class Bird {
  get plumage() { return "unknown"; }
}

class EuropeanSwallow extends Bird {
  get plumage() { return "average"; }
}

class AfricanSwallow extends Bird {
  get plumage() {
    return (this.numberOfCoconuts > 2) ? "tired" : "average";
  }
}

class NorwegianBlueParrot extends Bird {
  get plumage() {
    return (this.voltage > 100) ? "scorched" : "beautiful";
  }
}

function createBird(data) {
  switch (data.type) {
    case 'EuropeanSwallow': return new EuropeanSwallow(data);
    case 'AfricanSwallow': return new AfricanSwallow(data);
    case 'NorwegianBlueParrot': return new NorwegianBlueParrot(data);
    default: return new Bird(data);
  }
}
```

---

### 引入特例对象(Introduce Special Case / Null Object)

**适用场景**:反复对特殊情况进行 null 检查

**动机**:返回一个能处理特殊情况的特殊对象

**操作步骤**:
1. 创建具有预期接口的特殊情况类
2. 添加 isSpecialCase 检查
3. 引入工厂方法
4. 用特殊情况对象的用法替换 null 检查
5. 测试

**重构前**:
```javascript
const customer = site.customer;
// ... 多处检查
if (customer === "unknown") {
  customerName = "occupant";
} else {
  customerName = customer.name;
}
```

**重构后**:
```javascript
class UnknownCustomer {
  get name() { return "occupant"; }
  get billingPlan() { return registry.defaultPlan; }
}

// 工厂方法
function customer(site) {
  return site.customer === "unknown"
    ? new UnknownCustomer()
    : site.customer;
}

// 使用 -- 无需 null 检查
const customerName = customer.name;
```

---

## 重构 API(Refactoring APIs)

### 将查询与修饰符分离(Separate Query from Modifier)

**适用场景**:函数既返回值又有副作用

**动机**:明确哪些操作有副作用

**操作步骤**:
1. 创建一个新的查询函数
2. 复制原始函数的返回逻辑
3. 修改原始函数使其返回 void
4. 替换使用返回值的调用
5. 测试

**重构前**:
```javascript
function alertForMiscreant(people) {
  for (const p of people) {
    if (p === "Don") {
      setOffAlarms();
      return "Don";
    }
    if (p === "John") {
      setOffAlarms();
      return "John";
    }
  }
  return "";
}
```

**重构后**:
```javascript
function findMiscreant(people) {
  for (const p of people) {
    if (p === "Don") return "Don";
    if (p === "John") return "John";
  }
  return "";
}

function alertForMiscreant(people) {
  if (findMiscreant(people) !== "") setOffAlarms();
}
```

---

### 参数化函数(Parameterize Function)

**适用场景**:几个函数做类似的事情但使用不同的值

**动机**:通过添加参数来消除重复

**操作步骤**:
1. 选择其中一个函数
2. 为变化的部分添加参数
3. 修改函数体以使用该参数
4. 测试
5. 将调用方改为使用参数化版本
6. 移除现在无用的函数

**重构前**:
```javascript
function tenPercentRaise(person) {
  person.salary = person.salary * 1.10;
}

function fivePercentRaise(person) {
  person.salary = person.salary * 1.05;
}
```

**重构后**:
```javascript
function raise(person, factor) {
  person.salary = person.salary * (1 + factor);
}

// 使用方式
raise(person, 0.10);
raise(person, 0.05);
```

---

### 移除标志参数(Remove Flag Argument)

**适用场景**:改变函数行为的布尔参数

**动机**:通过独立的函数使行为显式化

**操作步骤**:
1. 为每个标志值创建显式的函数
2. 用适当的新函数替换每个调用
3. 每次更改后测试
4. 移除原始函数

**重构前**:
```javascript
function bookConcert(customer, isPremium) {
  if (isPremium) {
    // 高级预订逻辑
  } else {
    // 普通预订逻辑
  }
}

bookConcert(customer, true);
bookConcert(customer, false);
```

**重构后**:
```javascript
function bookPremiumConcert(customer) {
  // 高级预订逻辑
}

function bookRegularConcert(customer) {
  // 普通预订逻辑
}

bookPremiumConcert(customer);
bookRegularConcert(customer);
```

---

## 处理继承(Dealing with Inheritance)

### 上提方法(Pull Up Method)

**适用场景**:多个子类中有相同的方法

**动机**:消除类层级中的重复

**操作步骤**:
1. 检查方法确保它们完全相同
2. 检查签名是否一致
3. 在超类中创建新方法
4. 从一个子类复制方法体
5. 删除一个子类的方法,测试
6. 删除其他子类的方法,逐个测试

---

### 下推方法(Push Down Method)

**适用场景**:行为仅与部分子类相关

**动机**:将方法放在实际使用的地方

**操作步骤**:
1. 将方法复制到每个需要的子类
2. 从超类中移除方法
3. 测试
4. 从不需要的子类中移除
5. 测试

---

### 以委托取代子类(Replace Subclass with Delegate)

**适用场景**:继承被错误使用、需要更多灵活性时

**动机**:在适当时优先使用组合而非继承

**操作步骤**:
1. 为委托创建空类
2. 在宿主类中添加持有委托的字段
3. 创建委托的构造器,由宿主调用
4. 将功能移到委托
5. 每次移动后测试
6. 用委托替代继承

---

### 提取类(Extract Class)

**适用场景**:拥有多重职责的大类

**动机**:拆分类以保持单一职责

**操作步骤**:
1. 决定如何拆分职责
2. 创建新类
3. 将字段从原始类移到新类
4. 测试
5. 将方法从原始类移到新类
6. 每次移动后测试
7. 审查并重命名两个类
8. 决定如何暴露新类

**重构前**:
```javascript
class Person {
  get name() { return this._name; }
  set name(arg) { this._name = arg; }
  get officeAreaCode() { return this._officeAreaCode; }
  set officeAreaCode(arg) { this._officeAreaCode = arg; }
  get officeNumber() { return this._officeNumber; }
  set officeNumber(arg) { this._officeNumber = arg; }

  get telephoneNumber() {
    return `(${this._officeAreaCode}) ${this._officeNumber}`;
  }
}
```

**重构后**:
```javascript
class Person {
  constructor() {
    this._telephoneNumber = new TelephoneNumber();
  }
  get name() { return this._name; }
  set name(arg) { this._name = arg; }
  get telephoneNumber() { return this._telephoneNumber.toString(); }
  get officeAreaCode() { return this._telephoneNumber.areaCode; }
  set officeAreaCode(arg) { this._telephoneNumber.areaCode = arg; }
}

class TelephoneNumber {
  get areaCode() { return this._areaCode; }
  set areaCode(arg) { this._areaCode = arg; }
  get number() { return this._number; }
  set number(arg) { this._number = arg; }
  toString() { return `(${this._areaCode}) ${this._number}`; }
}
```

---

## 快速参考:异味 → 重构手法

| 代码异味 | 主要重构手法 | 备选方案 |
|----------|-------------|----------|
| Long Method(长方法) | Extract Method | Replace Temp with Query |
| Duplicate Code(重复代码) | Extract Method | Pull Up Method |
| Large Class(过大类) | Extract Class | Extract Subclass |
| Long Parameter List(过长参数列表) | Introduce Parameter Object | Preserve Whole Object |
| Feature Envy(特性依恋) | Move Method | Extract Method + Move |
| Data Clumps(数据泥团) | Extract Class | Introduce Parameter Object |
| Primitive Obsession(基本类型偏执) | Replace Primitive with Object | Replace Type Code |
| Switch Statements(Switch 语句) | Replace Conditional with Polymorphism | Replace Type Code |
| Temporary Field(临时字段) | Extract Class | Introduce Null Object |
| Message Chains(消息链) | Hide Delegate | Extract Method |
| Middle Man(中间人) | Remove Middle Man | Inline Method |
| Divergent Change(发散式变化) | Extract Class | Split Phase |
| Shotgun Surgery(霰弹式修改) | Move Method | Inline Class |
| Dead Code(死代码) | Remove Dead Code | - |
| Speculative Generality(抽象性过度泛化) | Collapse Hierarchy | Inline Class |

---

## 延伸阅读

- Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code* (2nd ed.)《重构:改善既有代码的设计》(第2版)
- 在线目录:https://refactoring.com/catalog/
