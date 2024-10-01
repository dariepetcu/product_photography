import { useState } from "react"
import { Button } from "src/components/ui/button"
import { Input } from "src/components/ui/input"
import { Label } from "src/components/ui/label"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "src/components/ui/card"
import { AlertCircle } from "lucide-react"
import { Alert, AlertDescription, AlertTitle } from "src/components/ui/alert"
import { useNavigate } from "react-router-dom"

export default function Component() {
  const [images, setImages] = useState<File[]>([])
  const [product_name, setProductName] = useState("")
  const [model_name, setModelName] = useState("")
  const [error, setError] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [successMessage, setSuccessMessage] = useState("")
  const navigate = useNavigate()

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    if (files.length < 5 || files.length > 20) {
      setError("Please select 5-20 images.")
      return
    }
    setImages(files)
    setError("")
  }

  const handleTextChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const words = e.target.value.trim().split(/\s+/)
    if (words.length > 2) {
      setError("Please enter 1-2 words only.")
      return
    }
    setProductName(e.target.value)
    setError("")
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)
    setError("")
    setSuccessMessage("")

    try {
      const formData = new FormData()
      images.forEach((image, index) => {
        formData.append(`image${index + 1}`, image)
      })
      formData.append("product_name", product_name)
      formData.append("model_name", model_name)

      const response = await fetch("http://127.0.0.1:5000/api/training", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const result = await response.json()
      setSuccessMessage("Form submitted successfully!")
      console.log("API Response:", result)
      navigate(`/model-training-status/${model_name}`)

    } catch (error) {
      setError("An error occurred while submitting the form. Please try again.")
      console.error("Submission error:", error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <Card className="w-full max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Image and Text Form</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="images">Upload 5-20 Images</Label>
            <Input
              id="images"
              type="file"
              accept="image/*"
              multiple
              onChange={handleImageChange}
              className="file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-primary-foreground hover:file:bg-primary/90"
            />
            {images.length > 0 && (
              <p className="text-sm text-muted-foreground">{images.length} images selected</p>
            )}
          </div>
          <div className="space-y-2">
            <Label htmlFor="text">Descibe the product in 1-2 Words</Label>
            <Input
              id="text"
              type="text"
              value={product_name}
              onChange={handleTextChange}
              placeholder="Enter 1-2 words"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="model_name">Model Name</Label>
            <Input
              id="model_name"
              type="text"
              value={model_name}
              onChange={(e) => setModelName(e.target.value)}
              placeholder="Enter model name"
            />
          </div>
        </form>
      </CardContent>
      <CardFooter className="flex flex-col items-start space-y-4">
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
        {successMessage && (
          <Alert variant="default">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Success</AlertTitle>
            <AlertDescription>{successMessage}</AlertDescription>
          </Alert>
        )}
        <Button 
          type="submit" 
          onClick={handleSubmit} 
          className="w-full" 
          disabled={isLoading}
        >
          {isLoading ? "Submitting..." : "Submit"}
        </Button>
      </CardFooter>
    </Card>
  )
}