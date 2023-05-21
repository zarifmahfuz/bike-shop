class Customer < ApplicationRecord
    validates :email, uniqueness: true, format: { with: URI::MailTo::EMAIL_REGEXP, message: "only allows valid emails" }
end
