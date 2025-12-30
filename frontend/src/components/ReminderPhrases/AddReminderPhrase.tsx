import {
  Button,
  createListCollection,
  DialogActionTrigger,
  DialogTitle,
  Input,
  Text,
  Textarea,
  VStack,
} from "@chakra-ui/react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { type SubmitHandler, useForm } from "react-hook-form"
import { FaPlus } from "react-icons/fa"

import { type ReminderPhraseCreate, MiddotService, ReminderPhrasesService } from "@/client"
import type { ApiError } from "@/client/core/ApiError"
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"
import {
  SelectContent,
  SelectItem,
  SelectRoot,
  SelectTrigger,
  SelectValueText,
} from "../ui/select"
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

const AddReminderPhrase = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [selectedMiddah, setSelectedMiddah] = useState<string[]>([])
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    setValue,
    formState: { errors, isValid, isSubmitting },
  } = useForm<ReminderPhraseCreate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      middah: "",
      text: "",
    },
  })

  const { data: middot, isLoading: isLoadingMiddot } = useQuery({
    queryFn: () => MiddotService.listMiddot(),
    queryKey: ["middot"],
  })

  const mutation = useMutation({
    mutationFn: (data: ReminderPhraseCreate) =>
      ReminderPhrasesService.createReminderPhrase({ requestBody: data }),
    onSuccess: () => {
      showSuccessToast("Reminder phrase created successfully.")
      reset()
      setSelectedMiddah([])
      setIsOpen(false)
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["reminderPhrases"] })
    },
  })

  const onSubmit: SubmitHandler<ReminderPhraseCreate> = (data) => {
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
        <Button value="add-reminder-phrase" my={4}>
          <FaPlus fontSize="16px" />
          Add Reminder Phrase
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Add Reminder Phrase</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Fill in the details to add a new reminder phrase.</Text>
            <VStack gap={4}>
              <Field
                required
                invalid={!!errors.middah}
                errorText={errors.middah?.message}
                label="Middah"
              >
                <SelectRoot
                  collection={createListCollection({
                    items: middot?.map(m => ({
                      label: `${m.name_transliterated} (${m.name_english})`,
                      value: m.name_transliterated,
                    })) ?? [],
                  })}
                  value={selectedMiddah}
                  onValueChange={(e) => {
                    setSelectedMiddah(e.value)
                    setValue("middah", e.value[0] || "", { shouldValidate: true })
                  }}
                  disabled={isLoadingMiddot}
                >
                  <SelectTrigger>
                    <SelectValueText placeholder="Select a middah" />
                  </SelectTrigger>
                  <SelectContent>
                    {middot?.map((middah) => (
                      <SelectItem key={middah.name_transliterated} item={middah.name_transliterated}>
                        {middah.name_transliterated} ({middah.name_english})
                      </SelectItem>
                    ))}
                  </SelectContent>
                </SelectRoot>
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
              disabled={!isValid}
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

export default AddReminderPhrase
