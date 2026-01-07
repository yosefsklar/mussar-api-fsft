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

import { type ApiError, type DailyTextRead, DailyTextsService } from "@/client"
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

interface EditDailyTextProps {
  dailyText: DailyTextRead
}

interface DailyTextUpdateForm {
  middah: string
  title: string | null
  sefaria_url: string | null
  content: string | null
}

const EditDailyText = ({ dailyText }: EditDailyTextProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<DailyTextUpdateForm>({
    mode: "onTouched",
    criteriaMode: "all",
    defaultValues: {
      middah: dailyText.middah,
      title: dailyText.title,
      sefaria_url: dailyText.sefaria_url,
      content: dailyText.content,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: DailyTextUpdateForm) =>
      DailyTextsService.patchDailyText({ 
        id: dailyText.id, 
        requestBody: data 
      }),
    onSuccess: () => {
      showSuccessToast("Daily text updated successfully.")
      reset()
      setIsOpen(false)
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["dailyTexts"] })
    },
  })

  const onSubmit: SubmitHandler<DailyTextUpdateForm> = async (data) => {
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
          Edit Daily Text
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Edit Daily Text</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Update the daily text details below.</Text>
            <VStack gap={4}>
              <Field
                required
                invalid={!!errors.middah}
                errorText={errors.middah?.message}
                label="Middah"
              >
                <Input
                  {...register("middah", {
                    required: "Middah is required",
                  })}
                  placeholder="e.g., Chesed"
                  type="text"
                />
              </Field>

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

export default EditDailyText
