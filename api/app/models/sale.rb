class Sale < ApplicationRecord
    validates :payment_method, inclusion: { in: ["cash", "credit/debit"],
        message: "%{value} is not a valid payment method" }
    validates :discount_percentage, numericality: { greater_than_or_equal_to: 0, 
        less_than_or_equal_to: 100, message: "is not in valid range" }
    # TODO: Define associations
end
