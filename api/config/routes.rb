Rails.application.routes.draw do
  # Define your application routes per the DSL in https://guides.rubyonrails.org/routing.html

  resources :bikes, only: %i[index create show update] do
    get 'analytics', on: :member
  end
end
