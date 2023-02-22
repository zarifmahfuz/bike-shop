import { Heading } from '@chakra-ui/react';
import { redirect, useLoaderData } from 'react-router-dom';

import { API_URL } from '../../../config';
import { Bike } from '../../models/bike';
import BikeForm from './BikeForm';

export default function EditBike() {
  const bike = useLoaderData() as Bike;
  return (
    <>
      <Heading as="h4" size="md">
        Update bike details
      </Heading>
      <BikeForm action="" bike={bike} />
    </>
  );
}

export const editBikeAction = async ({ request, params }) => {
  const { id } = params;
  const data = await request.formData();
  const submission = {
    name: data.get('name'),
    model: data.get('model'),
    price: data.get('price'),
    unitsAvailable: data.get('unitsAvailable'),
    description: data.get('description'),
    image: data.get('image'),
  };

  const res = await fetch(`${API_URL}/bikes/${id}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(submission),
  });

  const resData = await res.json();
  if (!res.ok) {
    return { error: resData.error[0].message };
  }
  return redirect(`/bikes/${id}`);
};
