class BikesController < ApplicationController
  before_action :set_bike, only: %i[show update]

  def index
    @bikes = Bike.search(params[:search])
  end

  def show; end

  def create
    @bike = Bike.new(bike_params)
    if @bike.save
      render :show, status: :created
    else
      render json: @bike.errors, status: :unprocessable_entity
    end
  end

  def update
    if @bike.update(bike_params)
      render :show
    else
      render json: @bike.errors, status: :unprocessable_entity
    end
  end

  private

  def set_bike
    @bike = Bike.find(params[:id])
  end

  def bike_params
    params.permit(:name, :model, :price, :units_available, :description, :image)
  end
end
