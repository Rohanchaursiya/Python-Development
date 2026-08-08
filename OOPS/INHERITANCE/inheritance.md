# Inheritance in Python

## Definition
Inheritance is a mechanism in object-oriented programming where a new class (child/derived class) acquires the properties and behaviors (attributes and methods) of an existing class (parent/base class). It promotes code reusability and establishes a hierarchical relationship between classes.

## Pros
- **Code Reusability**: Avoids duplicating code by inheriting existing functionality
- **Extensibility**: Easy to extend and modify existing classes without changing them
- **Maintainability**: Changes in base class automatically reflect in derived classes
- **Polymorphism Support**: Enables polymorphic behavior through method overriding
- **Logical Organization**: Models real-world hierarchical relationships naturally

## Cons
- **Tight Coupling**: Child classes become dependent on parent class implementation
- **Complexity**: Deep inheritance hierarchies can be difficult to understand and maintain
- **Fragile Base Class Problem**: Changes in base class may break derived classes
- **Inheritance Abuse**: Can lead to inappropriate hierarchies when composition is better
- **Performance Overhead**: Slight overhead due to method lookup in inheritance chain

## Use Cases
- **Framework Development**: Creating base classes for plugins/extensions (e.g., Django models)
- **UI Components**: Building widget hierarchies (Button → ClickableButton → SubmitButton)
- **Domain Modeling**: Representing taxonomic relationships (Animal → Mammal → Dog)
- **Template Method Pattern**: Defining algorithm skeleton in base class
- **Mixin Classes**: Adding reusable functionality to multiple unrelated classes

## Types of Inheritance (5 Types)
1. **Single Inheritance**
2. **Multiple Inheritance**
3. **Multilevel Inheritance**
4. **Hierarchical Inheritance**
5. **Hybrid Inheritance**