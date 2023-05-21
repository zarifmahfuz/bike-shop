# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.0].define(version: 2023_05_21_214259) do
  create_table "bike_sales", force: :cascade do |t|
    t.integer "units_sold", default: 1, null: false
    t.integer "units_refunded", default: 0, null: false
    t.decimal "price", precision: 7, scale: 2, null: false
    t.integer "bike_id", null: false
    t.integer "sale_id", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["bike_id"], name: "index_bike_sales_on_bike_id"
    t.index ["sale_id"], name: "index_bike_sales_on_sale_id"
  end

  create_table "bikes", force: :cascade do |t|
    t.string "name", null: false
    t.string "model", null: false
    t.decimal "price", precision: 7, scale: 2, null: false
    t.integer "units_available", default: 0, null: false
    t.text "description"
    t.text "image"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "customers", force: :cascade do |t|
    t.string "email", null: false
    t.string "first_name", null: false
    t.string "last_name", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "sales", force: :cascade do |t|
    t.datetime "sold_at", null: false
    t.string "payment_method", null: false
    t.decimal "total_sale", precision: 8, scale: 2
    t.integer "discount_percentage", default: 0
    t.integer "customer_id", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["customer_id"], name: "index_sales_on_customer_id"
  end

  add_foreign_key "bike_sales", "bikes"
  add_foreign_key "bike_sales", "sales"
  add_foreign_key "sales", "customers", on_delete: :restrict
end
