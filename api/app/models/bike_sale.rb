class BikeSale < ApplicationRecord
    validates :units_sold, numericality: { greater_than_or_equal_to: 0, message: "is not a valid value" }
    validates :units_refunded, numericality: { greater_than_or_equal_to: 0, message: "is not a valid value" }

    belongs_to :bike
    belongs_to :sale
end
