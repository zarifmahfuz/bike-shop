import { EditIcon } from '@chakra-ui/icons';
import {
  Box,
  Button,
  Container,
  Flex,
  Image,
  Spacer,
  Stack,
  Text,
} from '@chakra-ui/react';
import { useLoaderData, useNavigate } from 'react-router-dom';

import { API_URL } from '../../../config';
import { Bike } from '../../models/bike';

export default function BikeDetails() {
  const bike = useLoaderData() as Bike;
  console.log('Bike', bike);
  const navigate = useNavigate();
  return (
    <div>
      <Box maxW="480px" margin="15px">
        <Flex>
          <Box textAlign="center">
            <Text fontSize="2xl">
              {bike.name} | {bike.model}
            </Text>
          </Box>
          <Spacer />
          <Button
            color="white"
            bg="green.400"
            leftIcon={<EditIcon />}
            onClick={() => navigate('edit')}
          >
            Edit
          </Button>
        </Flex>
        <Image
          src={bike.image}
          alt="Image not available"
          borderRadius="md"
          marginY="10px"
        />
        <Stack mt="6" spacing="3">
          <Flex>
            <Text marginX="20px">${bike.price}</Text>
            <Spacer></Spacer>
            <Text marginX="20px">Units Available: {bike.unitsAvailable}</Text>
          </Flex>
          <Container>
            <Text color="gray.500">{bike.description}</Text>
          </Container>
        </Stack>
      </Box>
    </div>
  );
}

export const bikeDetailsLoader = async ({ params }) => {
  const { id } = params;
  const url = `${API_URL}/bikes/${id}/`;
  const res = await fetch(url);
  if (!res.ok) {
    // TODO: Bike not found
  }
  return res.json();
};
