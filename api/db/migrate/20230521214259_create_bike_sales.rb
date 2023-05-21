class CreateBikeSales < ActiveRecord::Migration[7.0]
  def change
    create_table :bike_sales do |t|
      t.integer :units_sold, null: false, default: 1
      t.integer :units_refunded, null: false, default: 0
      t.decimal :price, null: false, precision: 7, scale: 2, 
        comment: "Price at which the bike was sold at"
      t.belongs_to :bike, null: false, index: true, foreign_key: true
      t.belongs_to :sale, null: false, index: true, foreign_key: true

      t.timestamps
    end
  end
end
