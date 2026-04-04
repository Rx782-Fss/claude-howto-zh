# 代码异味（Code Smells）目录

基于 Martin Fowler《重构（Refactoring）》（第2版）的代码异味全面参考。代码异味是深层问题的表面征兆——它表明你的代码设计可能存在问题。

> "代码异味通常是系统中存在更深层次问题的表面指示。" — Martin Fowler

---

## 膨胀者（Bloaters）

表示某部分已经膨胀到难以有效处理的程度的代码异味。

### 长方法（Long Method）

**特征：**
- 方法超过 30-50 行
- 需要滚动才能看到完整方法
- 多层嵌套
- 需要注释来解释各部分的功能

**为什么不好：**
- 难以理解
- 难以单独测试
- 变更会产生意外后果
- 重复逻辑隐藏其中

**重构手法：**
- 提取方法（Extract Method）
- 以查询取代临时变量（Replace Temp with Query）
- 引入参数对象（Introduce Parameter Object）
- 以方法对象取代方法（Replace Method with Method Object）
- 分解条件表达式（Decompose Conditional）

**示例（重构前）：**
```javascript
function processOrder(order) {
  // 验证订单（20行）
  if (!order.items) throw new Error('No items');
  if (order.items.length === 0) throw new Error('Empty order');
  // ... 更多验证逻辑

  // 计算总额（30行）
  let subtotal = 0;
  for (const item of order.items) {
    subtotal += item.price * item.quantity;
  }
  // ... 税费、运费、折扣

  // 发送通知（20行）
  // ... 邮件逻辑
}
```

**示例（重构后）：**
```javascript
function processOrder(order) {
  validateOrder(order);
  const totals = calculateOrderTotals(order);
  sendOrderNotifications(order, totals);
  return { order, totals };
}
```

---

### 过大类（Large Class）

**特征：**
- 类拥有过多实例变量（>7-10 个）
- 类拥有过多方法（>15-20 个）
- 类名含糊不清（Manager、Handler、Processor）
- 方法并非都使用所有实例变量

**为什么不好：**
- 违反单一职责原则（Single Responsibility Principle）
- 难以测试
- 变更会波及不相关的功能
- 难以复用部分功能

**重构手法：**
- 提取类（Extract Class）
- 提取子类（Extract Subclass）
- 提取接口（Extract Interface）

**检测标准：**
```
代码行数 > 300
方法数量 > 15
字段数量 > 10
```

---

### 基本类型偏执（Primitive Obsession）

**特征：**
- 使用基本类型表示领域概念（用字符串表示邮箱，用整数表示金额）
- 使用基本类型数组而非对象
- 用字符串常量作为类型码
- 魔法数字/魔法字符串

**为什么不好：**
- 类型层面无法验证
- 逻辑散落在代码各处
- 容易传入错误值
- 缺少领域概念

**重构手法：**
- 以对象取代基本类型（Replace Primitive with Object）
- 以类取代类型码（Replace Type Code with Class）
- 以子类取代类型码（Replace Type Code with Subclasses）
- 以状态/策略取代类型码（Replace Type Code with State/Strategy）

**示例（重构前）：**
```javascript
const user = {
  email: 'john@example.com',     // 只是一个字符串
  phone: '1234567890',           // 只是一个字符串
  status: 'active',              // 魔法字符串
  balance: 10050                 // 用整数表示分（cents）
};
```

**示例（重构后）：**
```javascript
const user = {
  email: new Email('john@example.com'),
  phone: new PhoneNumber('1234567890'),
  status: UserStatus.ACTIVE,
  balance: Money.cents(10050)
};
```

---

### 过长参数列表（Long Parameter List）

**特征：**
- 方法有 4 个以上参数
- 参数总是成对出现
- 布尔标志改变方法行为
- 经常传递 null/undefined

**为什么不好：**
- 难以正确调用
- 参数顺序容易混淆
- 表明方法做了太多事情
- 难以添加新参数

**重构手法：**
- 引入参数对象（Introduce Parameter Object）
- 保持对象完整（Preserve Whole Object）
- 以方法调用取代参数（Replace Parameter with Method Call）
- 移除标志参数（Remove Flag Argument）

**示例（重构前）：**
```javascript
function createUser(firstName, lastName, email, phone,
                    street, city, state, zip,
                    isAdmin, isActive, createdBy) {
  // ...
}
```

**示例（重构后）：**
```javascript
function createUser(personalInfo, address, options) {
  // personalInfo: { firstName, lastName, email, phone }
  // address: { street, city, state, zip }
  // options: { isAdmin, isActive, createdBy }
}
```

---

### 数据泥团（Data Clumps）

**特征：**
- 相同的 3 个以上字段总是成组出现
- 参数总是结伴而行
- 类中存在属于同一组的字段子集

**为什么不好：**
- 重复的处理逻辑
- 缺少抽象
- 难以扩展
- 表明存在隐藏的类

**重构手法：**
- 提取类（Extract Class）
- 引入参数对象（Introduce Parameter Object）
- 保持对象完整（Preserve Whole Object）

**示例：**
```javascript
// 数据泥团：(x, y, z) 坐标
function movePoint(x, y, z, dx, dy, dz) { }
function scalePoint(x, y, z, factor) { }
function distanceBetween(x1, y1, z1, x2, y2, z2) { }

// 提取 Point3D 类
class Point3D {
  constructor(x, y, z) { }
  move(delta) { }
  scale(factor) { }
  distanceTo(other) { }
}
```

---

## 面向对象滥用者（Object-Orientation Abusers）

表明 OOP 原则使用不完整或不正确的异味。

### Switch 语句（Switch Statements）

**特征：**
- 过长的 switch/case 或 if/else 链
- 同一个 switch 出现在多个地方
- 基于 type code 的 switch
- 添加新 case 需要到处修改

**为什么不好：**
- 违反开闭原则（Open/Closed Principle）
- 变更会波及所有 switch 位置
- 难以扩展
- 通常表明缺少多态

**重构手法：**
- 以多态取代条件式（Replace Conditional with Polymorphism）
- 以子类取代类型码（Replace Type Code with Subclasses）
- 以状态/策略取代类型码（Replace Type Code with State/Strategy）

**示例（重构前）：**
```javascript
function calculatePay(employee) {
  switch (employee.type) {
    case 'hourly':
      return employee.hours * employee.rate;
    case 'salaried':
      return employee.salary / 12;
    case 'commissioned':
      return employee.sales * employee.commission;
  }
}
```

**示例（重构后）：**
```javascript
class HourlyEmployee {
  calculatePay() {
    return this.hours * this.rate;
  }
}

class SalariedEmployee {
  calculatePay() {
    return this.salary / 12;
  }
}
```

---

### 临时字段（Temporary Field）

**特征：**
- 实例变量只在某些方法中使用
- 字段被有条件地设置
- 特定情况需要复杂的初始化

**为什么不好：**
- 令人困惑——字段存在但可能为 null
- 难以理解对象状态
- 表明隐藏了条件逻辑

**重构手法：**
- 提取类（Extract Class）
- 引入 Null 对象（Introduce Null Object）
- 以局部变量取代临时字段（Replace Temp Field with Local）

---

### 被拒绝的遗赠（Refused Bequest）

**特征：**
- 子类未使用继承的方法/数据
- 子类覆写方法但什么都不做
- 继承被用于代码复用，而非 IS-A 关系

**为什么不好：**
- 错误的抽象
- 违反里氏替换原则（Liskov Substitution Principle）
- 误导性的继承层级

**重构手法：**
- 下推方法/字段（Push Down Method/Field）
- 以委托取代子类（Replace Subclass with Delegate）
- 以委托取代继承（Replace Inheritance with Delegation）

---

### 异曲同工的类（Alternative Classes with Different Interfaces）

**特征：**
- 两个类做类似的事情
- 相同概念使用不同的方法名
- 可以互换使用

**为什么不好：**
- 重复实现
- 没有共同接口
- 难以在两者间切换

**重构手法：**
- 重命名方法（Rename Method）
- 搬移方法（Move Method）
- 提取超类（Extract Superclass）
- 提取接口（Extract Interface）

---

## 变更阻碍者（Change Preventers）

使变更变得困难的异味——改一处需要改很多处。

### 发散式变化（Divergent Change）

**特征：**
- 一个类因多种不同原因而需要修改
- 不同领域的变更触发同一类的编辑
- 类变成了"上帝类"（God class）

**为什么不好：**
- 违反单一职责原则
- 高变更频率
- 合并冲突频繁

**重构手法：**
- 提取类（Extract Class）
- 提取超类（Extract Superclass）
- 提取子类（Extract Subclass）

**示例：**
`User` 类因以下原因需要修改：
- 认证相关变更
- 个人资料相关变更
- 账单相关变更
- 通知相关变更

→ 提取为：`AuthService`、`ProfileService`、`BillingService`、`NotificationService`

---

### 霰弹式修改（Shotgun Surgery）

**特征：**
- 一处变更需要在多个类中编辑
- 一个小功能需要改动 10+ 文件
- 变更分散，难以找全

**为什么不好：**
- 容易遗漏
- 高耦合
- 变更容易出错

**重构手法：**
- 搬移方法（Move Method）
- 搬移字段（Move Field）
- 内联类（Inline Class）

**检测方法：**
观察是否出现：添加一个字段需要在 5 个以上文件中进行修改。

---

### 平行继承体系（Parallel Inheritance Hierarchies）

**特征：**
- 在一个体系中创建子类需要在另一个中也创建
- 类前缀匹配（如 `DatabaseOrder`、`DatabaseProduct`）

**为什么不好：**
- 维护工作量翻倍
- 体系之间产生耦合
- 容易遗漏一侧

**重构手法：**
- 搬移方法（Move Method）
- 搬移字段（Move Field）
- 消除其中一个继承体系

---

## 冗余物（Dispensables）

应该被移除的不必要之物。

### 过多的注释（Comments — Excessive）

**特征：**
- 注释解释代码做什么
- 被注释掉的代码
- 永远停留的 TODO/FIXME
- 注释中的道歉

**为什么不好：**
- 注释会撒谎（与代码不同步）
- 代码应该是自文档化的
- 死代码造成困惑

**重构手法：**
- 提取方法（Extract Method）——用名称说明用途
- 重命名（Rename）——无需注释即可清晰表达
- 移除注释掉的代码
- 引入断言（Introduce Assertion）

**好注释 vs 坏注释：**
```javascript
// 坏：解释"做什么"
// 遍历用户并检查是否活跃
for (const user of users) {
  if (user.status === 'active') { }
}

// 好：解释"为什么"
// 仅活跃用户 — 不活跃用户由清理任务处理
const activeUsers = users.filter(u => u.isActive);
```

---

### 重复代码（Duplicate Code）

**特征：**
- 相同代码出现在多处
- 有微小差异的相似代码
- 复制粘贴模式

**为什么不好：**
- Bug 修复需要在多处进行
- 存在不一致风险
- 代码库臃肿

**重构手法：**
- 提取方法（Extract Method）
- 提取类（Extract Class）
- 上提方法（Pull Up Method）（在继承体系中）
- 形成模板方法（Form Template Method）

**检测规则：**
任何重复 3 次及以上的代码都应该被提取。

---

### 冗余类（Lazy Class）

**特征：**
- 类做得太少，不足以证明其存在的价值
- 没有附加价值的包装器
- 过度设计的产物

**为什么不好：**
- 维护开销
- 不必要的间接层
- 徒增复杂度而无收益

**重构手法：**
- 内联类（Inline Class）
- 折叠继承体系（Collapse Hierarchy）

---

### 死代码（Dead Code）

**特征：**
- 不可达代码
- 未使用的变量/方法/类
- 被注释掉的代码
- 不可能条件后的代码

**为什么不好：**
- 造成困惑
- 维护负担
- 减慢理解速度

**重构手法：**
- 移除死代码（Remove Dead Code）
- 安全删除（Safe Delete）

**检测方法：**
```bash
# 查找未使用的导出
# 查找未被引用的函数
# IDE 的 "unused" 警告
```

---

### 抽象性过度的泛化（Speculative Generality）

**特征：**
- 只有一个子类的抽象类
- "为将来使用"的未使用参数
- 只做委托的方法
- 只用于一个用例的"框架"

**为什么不好：**
- 徒增复杂度而无收益
- YAGNI 原则（You Ain't Gonna Need It，你并不需要它）
- 更难理解

**重构手法：**
- 折叠继承体系（Collapse Hierarchy）
- 内联类（Inline Class）
- 移除参数（Remove Parameter）
- 重命名方法（Rename Method）

---

## 耦合者（Couplers）

表示类之间存在过度耦合的异味。

### 特性依恋（Feature Envy）

**特征：**
- 方法更多地使用了另一个类的数据而非自身数据
- 大量调用另一个对象的 getter
- 数据和行为分离

**为什么不好：**
- 行为位置不当
- 封装不良
- 难以维护

**重构手法：**
- 搬移方法（Move Method）
- 搬移字段（Move Field）
- 提取方法（Extract Method）（然后搬移）

**示例（重构前）：**
```javascript
class Order {
  getDiscountedPrice(customer) {
    // 大量使用 customer 的数据
    if (customer.loyaltyYears > 5) {
      return this.price * customer.discountRate;
    }
    return this.price;
  }
}
```

**示例（重构后）：**
```javascript
class Customer {
  getDiscountedPriceFor(price) {
    if (this.loyaltyYears > 5) {
      return price * this.discountRate;
    }
    return price;
  }
}
```

---

### 不当亲密（Inappropriate Intimacy）

**特征：**
- 类之间互相访问私有成员
- 双向引用
- 子类对父类了解太多

**为什么不好：**
- 高耦合
- 变更级联扩散
- 难以独立修改一方

**重构手法：**
- 搬移方法（Move Method）
- 搬移字段（Move Field）
- 将双向改为单向引用（Change Bidirectional to Unidirectional）
- 提取类（Extract Class）
- 隐藏委托（Hide Delegate）

---

### 消息链（Message Chains）

**特征：**
- 过长的方法调用链：`a.getB().getC().getD().getValue()`
- 客户端依赖导航结构
- "列车失事"式的代码

**为什么不好：**
- 脆弱——任何变更都会打断链
- 违反得墨忒尔法则（Law of Demeter）
- 与结构耦合

**重构手法：**
- 隐藏委托（Hide Delegate）
- 提取方法（Extract Method）
- 搬移方法（Move Method）

**示例：**
```javascript
// 差：消息链
const managerName = employee.getDepartment().getManager().getName();

// 好：隐藏委托
const managerName = employee.getManagerName();
```

---

### 中间人（Middle Man）

**特征：**
- 类只做委托给另一个类的工作
- 一半方法是委托操作
- 没有附加价值

**为什么不好：**
- 不必要的间接层
- 维护开销
- 架构令人困惑

**重构手法：**
- 移除中间人（Remove Middle Man）
- 内联方法（Inline Method）

---

## 异味严重程度指南

| 严重程度 | 描述 | 应对措施 |
|----------|------|----------|
| **Critical（严重）** | 阻碍开发，引发 Bug | 立即修复 |
| **High（高）** | 显著的维护负担 | 在当前迭代中修复 |
| **Medium（中）** | 明显但可管理 | 计划近期处理 |
| **Low（低）** | 微小不便 | 见缝插针地修复 |

---

## 快速检测清单

扫描代码时使用此清单：

- [ ] 是否有超过 30 行的方法？
- [ ] 是否有超过 300 行的类？
- [ ] 是否有超过 4 个参数的方法？
- [ ] 是否有重复的代码块？
- [ ] 是否有基于类型码的 switch/case？
- [ ] 是否有未使用的代码？
- [ ] 是否有大量使用其他类数据的方法？
- [ ] 是否有过长的方法调用链？
- [ ] 是否有解释"做什么"而非"为什么"的注释？
- [ ] 是否有应该成为对象的基本类型？

---

## 延伸阅读

- Fowler, M. (2018). *Refactoring: Improving the Design of Existing Code* (2nd ed.)《重构：改善既有代码的设计》（第2版）
- Kerievsky, J. (2004). *Refactoring to Patterns*《重构与模式》
- Feathers, M. (2004). *Working Effectively with Legacy Code*《修改代码的艺术》
