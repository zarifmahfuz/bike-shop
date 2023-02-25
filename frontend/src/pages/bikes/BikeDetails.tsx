import { EditIcon } from '@chakra-ui/icons';
import {
  Box,
  Button,
  Card,
  CardBody,
  CardHeader,
  Flex,
  Grid,
  GridItem,
  Heading,
  Image,
  Spacer,
  Stack,
  StackDivider,
  Text,
} from '@chakra-ui/react';
import { redirect, useLoaderData, useNavigate } from 'react-router-dom';

import { API_URL } from '../../../config';
import { Bike } from '../../models/bike';
import BikeAnalytics from './BikeAnalytics';

export default function BikeDetails() {
  const bike = useLoaderData() as Bike;
  const navigate = useNavigate();
  return (
    <Box maxW="100%">
      <Flex>
        <Heading as="h2" size="lg">
          Bike Details
        </Heading>
        <Spacer />
        <Button bg="#85C894" leftIcon={<EditIcon />} onClick={() => navigate('edit')}>
          Edit
        </Button>
      </Flex>

      <Grid templateColumns="repeat(6, 1fr)">
        <GridItem
          colSpan={{ base: 6, md: 4 }}
          minHeight={{ lg: '100vh' }}
          padding={{ base: '20px', lg: '30px' }}
        >
          <Card>
            <CardHeader>
              <Heading size="md">
                {bike.name} | {bike.model}
              </Heading>
            </CardHeader>
            <CardBody>
              <Stack divider={<StackDivider />} spacing={4}>
                <Box>
                  <Flex justify="space-around">
                    <Image
                      src={bike.image}
                      alt="Image not available"
                      borderRadius="md"
                      marginY="10px"
                      maxWidth="400px"
                    />
                  </Flex>
                </Box>
                <Box>
                  <Flex justify="space-around" gap={4}>
                    <Text marginX="20px">${bike.price}</Text>
                    <Text marginX="20px">Units Available: {bike.unitsAvailable}</Text>
                  </Flex>
                </Box>
                <Box>
                  <Text color="gray.500">{bike.description}</Text>
                </Box>
              </Stack>
            </CardBody>
          </Card>
        </GridItem>
        <GridItem
          colSpan={{ base: 6, md: 2 }}
          padding={{ base: '20px', lg: '30px' }}
          minHeight={{ lg: '100vh' }}
        >
          <BikeAnalytics bikeId={bike.id} />
        </GridItem>
      </Grid>
    </Box>
  );
}

export const bikeDetailsLoader = async ({ params }) => {
  const { id } = params;
  const url = `${API_URL}/bikes/${id}/`;
  const res = await fetch(url);
  if (!res.ok) {
    return redirect('/error');
  }
  return res.json();
};
