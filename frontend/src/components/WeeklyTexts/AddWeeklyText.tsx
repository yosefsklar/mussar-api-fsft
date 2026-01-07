import {
  Button,
  DialogActionTrigger,
  DialogTitle,
  Input,
  Textarea,
  Text,
  VStack,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { type SubmitHandler, useForm } from "react-hook-form"
import { FaPlus } from "react-icons/fa"

import { type WeeklyTextCreate, WeeklyTextsService } from "@/client"
import type { ApiError } from "@/client/core/ApiError"
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"
import {
  DialogBody,
  DialogCloseTrigger,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogRoot,
  DialogTrigger,
} from "../ui/dialog"
import { Field } from "../ui/field"

const AddWeeklyText = () => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<WeeklyTextCreate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      sefaria_url: null,
      title: null,
      content: null,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: WeeklyTextCreate) =>
      WeeklyTextsService.createWeeklyText({ requestBody: data }),
    onSuccess: () => {
      showSuccessToast("Weekly text created successfully.")
      reset()
      setIsOpen(false)
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["weeklyTexts"] })
    },
  })

  const onSubmit: SubmitHandler<WeeklyTextCreate> = (data) => {
    mutation.mutate(data)
  }

  return (
    <DialogRoot
      size={{ base: "xs", md: "md" }}
      placement="center"
      open={isOpen}
      onOpenChange={({ open }) => setIsOpen(open)}
    >
      <DialogTrigger asChild>
        <Button value="add-weekly-text" my={4}>
          <FaPlus fontSize="16px" />
          Add Weekly Text
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Add Weekly Text</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Fill in the details to add a new weekly text.</Text>
            <VStack gap={4}>
              <Field
                invalid={!!errors.title}
                errorText={errors.title?.message}
                label="Title"
              >
                <Input
                  {...register("title")}
                  placeholder="Enter title (optional)"
                />
              </Field>

              <Field
                invalid={!!errors.sefaria_url}
                errorText={errors.sefaria_url?.message}
                label="Sefaria URL"
              >
                <Input
                  {...register("sefaria_url")}
                  placeholder="Enter Sefaria URL (optional)"
                />
              </Field>

              <Field
                invalid={!!errors.content}
                errorText={errors.content?.message}
                label="Content"
              >
                <Textarea
                  {...register("content")}
                  placeholder="Enter content (optional)"
                  rows={4}
                />
              </Field>
            </VStack>
          </DialogBody>

          <DialogFooter gap={2}>
            <DialogActionTrigger asChild>
              <Button
                variant="subtle"
                colorPalette="gray"
                disabled={isSubmitting}
              >
                Cancel
              </Button>
            </DialogActionTrigger>
            <Button
              variant="solid"
              type="submit"
              loading={isSubmitting}
            >
              Save
            </Button>
          </DialogFooter>
        </form>
        <DialogCloseTrigger />
      </DialogContent>
    </DialogRoot>
  )
}

export default AddWeeklyText
