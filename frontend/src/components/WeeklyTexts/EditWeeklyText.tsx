import {
  Button,
  ButtonGroup,
  DialogActionTrigger,
  Input,
  Textarea,
  Text,
  VStack,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { type SubmitHandler, useForm } from "react-hook-form"
import { FaExchangeAlt } from "react-icons/fa"

import { type ApiError, type WeeklyTextRead, WeeklyTextsService } from "@/client"
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"
import {
  DialogBody,
  DialogCloseTrigger,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogRoot,
  DialogTitle,
  DialogTrigger,
} from "../ui/dialog"
import { Field } from "../ui/field"

interface EditWeeklyTextProps {
  weeklyText: WeeklyTextRead
}

interface WeeklyTextUpdateForm {
  title: string | null
  sefaria_url: string | null
  content: string | null
}

const EditWeeklyText = ({ weeklyText }: EditWeeklyTextProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<WeeklyTextUpdateForm>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      title: weeklyText.title,
      sefaria_url: weeklyText.sefaria_url,
      content: weeklyText.content,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: WeeklyTextUpdateForm) =>
      WeeklyTextsService.patchWeeklyText({ 
        id: weeklyText.id, 
        requestBody: data 
      }),
    onSuccess: () => {
      showSuccessToast("Weekly text updated successfully.")
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

  const onSubmit: SubmitHandler<WeeklyTextUpdateForm> = async (data) => {
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
        <Button variant="ghost">
          <FaExchangeAlt fontSize="16px" />
          Edit Weekly Text
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Edit Weekly Text</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Update the weekly text details below.</Text>
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
            <ButtonGroup>
              <DialogActionTrigger asChild>
                <Button
                  variant="subtle"
                  colorPalette="gray"
                  disabled={isSubmitting}
                >
                  Cancel
                </Button>
              </DialogActionTrigger>
              <Button variant="solid" type="submit" loading={isSubmitting}>
                Save
              </Button>
            </ButtonGroup>
          </DialogFooter>
        </form>
        <DialogCloseTrigger />
      </DialogContent>
    </DialogRoot>
  )
}

export default EditWeeklyText
