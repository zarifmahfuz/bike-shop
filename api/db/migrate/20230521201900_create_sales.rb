class CreateSales < ActiveRecord::Migration[7.0]
  def change
    create_table :sales do |t|
      t.datetime :sold_at, null: false
      t.string :payment_method, null: false
      t.decimal :total_sale, precision: 8, scale: 2
      t.integer :discount_percentage, default: 0
      t.references :customer, null: false, foreign_key: { on_delete: :restrict }

      t.timestamps
    end
  end
end
