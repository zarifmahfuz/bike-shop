import { Heading } from '@chakra-ui/react';
import { redirect } from 'react-router-dom';

import { API_URL } from '../../../config';
import BikeForm from './BikeForm';

export default function AddBike() {
  return (
    <>
      <Heading as="h4" size="md">
        Add a new bike
      </Heading>
      <BikeForm action="/bikes/new" />
    </>
  );
}

export const createBikeAction = async ({ request }) => {
  const data = await request.formData();
  const submission = {
    name: data.get('name'),
    model: data.get('model'),
    price: data.get('price'),
    unitsAvailable: data.get('unitsAvailable'),
    description: data.get('description'),
    image: data.get('image'),
  };

  const res = await fetch(`${API_URL}/bikes/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(submission),
  });
  const resData = await res.json();
  if (!res.ok) {
    return { error: resData.error[0].message };
  }
  return redirect('/bikes');
};
