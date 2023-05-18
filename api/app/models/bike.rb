require 'uri'

class Bike < ApplicationRecord
    validates :units_available, numericality: { greater_than_or_equal_to: 0 }
    validates :image, format: { with: URI::DEFAULT_PARSER.make_regexp, message: "Invalid URL format" }, if: -> { image.present? }
end
