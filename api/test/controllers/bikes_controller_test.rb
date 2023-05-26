require 'test_helper'

class BikesControllerTest < ActionDispatch::IntegrationTest
  setup do
    @bike_one = bikes(:one)
    @bike_two = bikes(:two)
  end

  test 'should get index' do
    get bikes_url, as: :json
    assert_response :success
    assert_equal 2, JSON.parse(response.body).length
  end

  test 'should get index with search' do
    get "#{bikes_url}?search=Trek", as: :json
    assert_response :success
    assert_equal 1, JSON.parse(response.body).length
    assert_equal @bike_one.name, JSON.parse(response.body).first['name']
  end

  test 'bike not found' do
    get bike_url(3000), as: :json
    assert_response :not_found
  end

  test 'should create bike' do
    assert_difference('Bike.count') do
      post bikes_url,
           params: { name: 'Test Bike', model: 'Test Model', price: 300.00, units_available: 5,
                     description: 'Test description', image: 'https://example.com/test.jpg' }, as: :json
    end
    assert_response :created
    response_json = JSON.parse(response.body)
    assert_equal 'Test Bike', response_json['name']
  end

  test 'should show bike' do
    get bike_url(@bike_one), as: :json
    assert_response :success
    response_json = JSON.parse(response.body)
    assert_equal @bike_one.name, response_json['name']
  end

  test 'should update bike' do
    patch bike_url(@bike_one), params: { name: 'Updated Bike' }, as: :json
    @bike_one.reload
    assert_equal 'Updated Bike', @bike_one.name
    assert_response :success
  end

  test 'should not create bike with invalid params' do
    assert_no_difference('Bike.count') do
      post bikes_url, params: { name: '', model: 'Test Model', price: 300.00, units_available: 5,
                                description: 'Test description', image: 'https://example.com/test.jpg' }, as: :json
    end
    assert_response :unprocessable_entity
  end

  test 'should not update bike with invalid params' do
    patch bike_url(@bike_one), params: { name: '' }, as: :json
    @bike_one.reload
    assert_not_equal '', @bike_one.name
    assert_response :unprocessable_entity
  end

  test 'should not update bike id' do
    patch bike_url(@bike_one), params: { id: 4 }, as: :json
    @bike_one.reload
    assert_not_equal 4, @bike_one.id
    assert_response :success
  end
end
