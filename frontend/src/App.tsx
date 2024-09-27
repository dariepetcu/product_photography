import React from 'react';
import { ChakraProvider, Box, VStack, Heading } from '@chakra-ui/react';
import ModelTrainingForm from './components/ModelTrainingForm';

function App() {
  return (
    <ChakraProvider>
      <Box p={8}>
        <VStack spacing={8}>
          <Heading>Product Photo AI</Heading>
          <ModelTrainingForm />
        </VStack>
      </Box>
    </ChakraProvider>
  );
}

export default App;