import {
  Button,
  ButtonGroup,
  DialogActionTrigger,
  Input,
  Text,
  Textarea,
  VStack,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { type SubmitHandler, useForm } from "react-hook-form"
import { FaExchangeAlt } from "react-icons/fa"

import { type ApiError, type ReminderPhraseRead, ReminderPhrasesService } from "@/client"
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

interface EditReminderPhraseProps {
  reminderPhrase: ReminderPhraseRead
}

interface ReminderPhraseUpdateForm {
  middah: string
  text: string
}

const EditReminderPhrase = ({ reminderPhrase }: EditReminderPhraseProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<ReminderPhraseUpdateForm>({
    mode: "onTouched",
    criteriaMode: "all",
    defaultValues: {
      middah: reminderPhrase.middah,
      text: reminderPhrase.text,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: ReminderPhraseUpdateForm) =>
      ReminderPhrasesService.patchReminderPhrase({ 
        id: reminderPhrase.id, 
        requestBody: data 
      }),
    onSuccess: () => {
      showSuccessToast("Reminder phrase updated successfully.")
      reset()
      setIsOpen(false)
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["reminderPhrases"] })
    },
  })

  const onSubmit: SubmitHandler<ReminderPhraseUpdateForm> = async (data) => {
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
          Edit Reminder Phrase
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Edit Reminder Phrase</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Update the reminder phrase details below.</Text>
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
                required
                invalid={!!errors.text}
                errorText={errors.text?.message}
                label="Text"
              >
                <Input
                  {...register("text", {
                    required: "Text is required.",
                  })}
                  placeholder="Enter reminder phrase text"
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault()
                      handleSubmit(onSubmit)()
                    }
                  }}
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

export default EditReminderPhrase
