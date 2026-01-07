import {
  Button,
  createListCollection,
  DialogActionTrigger,
  DialogTitle,
  Input,
  Textarea,
  Text,
  VStack,
} from "@chakra-ui/react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { type SubmitHandler, useForm } from "react-hook-form"
import { FaPlus } from "react-icons/fa"

import { type DailyTextCreate, DailyTextsService, MiddotService } from "@/client"
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

const AddDailyText = () => {
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
  } = useForm<DailyTextCreate>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      middah: "",
      sefaria_url: null,
      title: null,
      content: null,
    },
  })

  const { data: middot, isLoading: isLoadingMiddot } = useQuery({
    queryFn: () => MiddotService.listMiddot(),
    queryKey: ["middot"],
  })

  const mutation = useMutation({
    mutationFn: (data: DailyTextCreate) =>
      DailyTextsService.createDailyText({ requestBody: data }),
    onSuccess: () => {
      showSuccessToast("Daily text created successfully.")
      reset()
      setSelectedMiddah([])
      setIsOpen(false)
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["dailyTexts"] })
    },
  })

  const onSubmit: SubmitHandler<DailyTextCreate> = (data) => {
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
        <Button value="add-daily-text" my={4}>
          <FaPlus fontSize="16px" />
          Add Daily Text
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Add Daily Text</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Fill in the details to add a new daily text.</Text>
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

export default AddDailyText
