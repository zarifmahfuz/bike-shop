class Bike < ApplicationRecord
  validates :units_available, numericality: { greater_than_or_equal_to: 0 }
  validates :image, format: { with: URI::DEFAULT_PARSER.make_regexp, message: 'Invalid URL format' },
                    if: -> { image.present? }
  validates :name, :model, :price, :units_available, presence: true
  has_many :bike_sales
  has_many :sales, through: :bike_sales

  class << self
    def search(search)
      if search
        where('name LIKE ? OR model LIKE ?', "%#{search}%", "%#{search}%")
      else
        all
      end
    end
  end
end
