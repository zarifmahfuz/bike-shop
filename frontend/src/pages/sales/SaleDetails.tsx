import { Box, Button, Flex, Grid, GridItem, Heading, Spacer } from '@chakra-ui/react';
import { useLoaderData, useNavigate } from 'react-router-dom';

import { API_URL } from '../../../config';
import { Sale } from '../../models/sale';
import BikeSaleInfoCard from './BikeSaleInfoCard';
import SaleInfoCard from './SaleInfoCard';

export default function SaleDetails() {
  const sale = useLoaderData() as Sale;
  const navigate = useNavigate();
  const deleteSale = async () => {
    const url = `${API_URL}/sales/${sale.id}/`;
    const res = await fetch(url, {
      method: 'DELETE',
    });
    if (res.ok) {
      return navigate('/sales');
    } else {
      // TODO: Something went wrong
    }
  };
  return (
    <Box maxWidth="100%">
      <Flex>
        <Heading as="h2" size="lg">
          Sale Details
        </Heading>
        <Spacer />
        <Button bg="red.400" onClick={deleteSale}>
          Delete Sale
        </Button>
      </Flex>

      <Grid templateColumns="repeat(7, 1fr)">
        <GridItem
          colSpan={{ base: 7, md: 3 }}
          minHeight={{ lg: '100vh' }}
          padding={{ base: '20px', lg: '30px' }}
        >
          <SaleInfoCard sale={sale} />
        </GridItem>

        <GridItem
          colSpan={{ base: 7, md: 4 }}
          padding={{ base: '20px', lg: '30px' }}
          minHeight={{ lg: '100vh' }}
        >
          <BikeSaleInfoCard sale={sale} />
        </GridItem>
      </Grid>
    </Box>
  );
}

export const saleDetailsLoader = async ({ params }) => {
  const { id } = params;
  const url = `${API_URL}/sales/${id}/`;
  const res = await fetch(url);
  if (!res.ok) {
    // TODO: Sale not found
  }
  return res.json();
};
