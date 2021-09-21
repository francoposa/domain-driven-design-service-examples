use rust_decimal::Decimal;
use rust_decimal_macros::dec;
use uuid::Uuid;

pub struct Order {
    pub order_id: Uuid,
    pub customer_id: Uuid,
    pub items: Vec<ProductOrderItem>,
}

impl Order {
    pub fn total(&self) -> Decimal {
        self.items.iter().map(|x| x.total()).sum()
    }
}

pub struct ProductOrderItem {
    pub order_id: Uuid,
    pub product_id: Uuid,
    pub quantity: Decimal,
    pub unit_price: Decimal,
}

impl ProductOrderItem {
    fn order_id(&self) -> Uuid {
        self.order_id
    }

    fn total(&self) -> Decimal {
        self.quantity * self.unit_price
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_total() {
        let product_order_item_0 = ProductOrderItem {
            order_id: Uuid::new_v4(),
            product_id: Uuid::new_v4(),
            quantity: dec!(1),
            unit_price: dec!(2.00),
        };

        let order = Order {
            order_id: Uuid::new_v4(),
            customer_id: Uuid::new_v4(),
            items: vec![product_order_item_0],
        };

        assert_eq!(order.total(), dec!(2))
    }
}
