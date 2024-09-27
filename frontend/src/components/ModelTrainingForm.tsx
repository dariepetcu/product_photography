import React, { useState } from 'react';
import {
  Button,
  Card,
  CardBody,
  CardHeader,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Heading,
  useToast,
  Text,
} from '@chakra-ui/react';

const ModelTrainingForm: React.FC = () => {
  const [images, setImages] = useState<File[]>([]);
  const [productName, setProductName] = useState('');
  const [modelName, setModelName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const files = Array.from(e.target.files);
      setImages(files);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);

    if (images.length < 5 || images.length > 10) {
      toast({
        title: "Invalid number of images",
        description: "Please upload between 5 and 10 images.",
        status: "error",
        duration: 5000,
        isClosable: true,
      });
      setIsLoading(false);
      return;
    }

    const formData = new FormData();
    images.forEach((image, index) => {
      formData.append(`image_${index}`, image);
    });
    formData.append('product_name', productName);
    formData.append('model_name', modelName);

    try {
      console.log("Sending request to /api/training");
      console.log("FormData contents:", Object.fromEntries(formData));

      const response = await fetch('/api/training', {
        method: 'POST',
        body: formData,
      });

      console.log("Response status:", response.status);
      console.log("Response headers:", response.headers);

      const responseText = await response.text();
      console.log("Response text:", responseText);

      let result;
      try {
        result = JSON.parse(responseText);
      } catch (parseError) {
        console.error("Error parsing JSON:", parseError);
        throw new Error("Invalid JSON response from server: ${responseText}");
      }

      if (response.ok) {
        toast({
          title: "Success",
          description: `Model created and trained successfully! Model ID: ${result.model_id}`,
          status: "success",
          duration: 5000,
          isClosable: true,
        });
      } else {
        throw new Error(result.error || 'Unknown server error');
      }
    } catch (error) {
      console.error('Error:', error);
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : 'An unknown error occurred',
        status: "error",
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card maxW="md" mx="auto">
      <CardHeader>
        <Heading size="lg">Model Training Form</Heading>
      </CardHeader>
      <CardBody>
        <form onSubmit={handleSubmit}>
          <VStack spacing={4}>
            <FormControl>
              <FormLabel htmlFor="images">Upload Images (5-10)</FormLabel>
              <Input
                id="images"
                type="file"
                accept="image/*"
                multiple
                onChange={handleImageChange}
                required
              />
              <Text fontSize="sm" color="gray.500" mt={1}>
                {images.length} image(s) selected
              </Text>
            </FormControl>
            <FormControl>
              <FormLabel htmlFor="productName">Product Name (1-2 words)</FormLabel>
              <Input
                id="productName"
                type="text"
                value={productName}
                onChange={(e) => setProductName(e.target.value)}
                required
              />
            </FormControl>
            <FormControl>
              <FormLabel htmlFor="modelName">Model Name</FormLabel>
              <Input
                id="modelName"
                type="text"
                value={modelName}
                onChange={(e) => setModelName(e.target.value)}
                required
              />
            </FormControl>
            <Button 
              type="submit" 
              colorScheme="blue" 
              width="full"
              isLoading={isLoading}
              loadingText="Submitting"
            >
              Submit
            </Button>
          </VStack>
        </form>
      </CardBody>
    </Card>
  );
};

export default ModelTrainingForm;