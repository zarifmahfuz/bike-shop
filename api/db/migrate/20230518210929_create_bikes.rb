class CreateBikes < ActiveRecord::Migration[7.0]
  def change
    create_table :bikes do |t|
      t.string :name, null: false
      t.string :model, null: false
      t.decimal :price, precision: 7, scale: 2, null: false
      t.integer :units_available, default: 0, null: false
      t.text :description
      t.text :image

      t.timestamps
    end
  end
end
