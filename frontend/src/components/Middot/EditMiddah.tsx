import {
  Button,
  ButtonGroup,
  DialogActionTrigger,
  Input,
  Text,
  VStack,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { type SubmitHandler, useForm } from "react-hook-form"
import { FaExchangeAlt } from "react-icons/fa"

import { type ApiError, type MiddahRead, MiddotService } from "@/client"
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

interface EditMiddahProps {
  middah: MiddahRead
}

interface MiddahUpdateForm {
  name_hebrew: string
  name_english: string
}

const EditMiddah = ({ middah }: EditMiddahProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<MiddahUpdateForm>({
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      name_hebrew: middah.name_hebrew,
      name_english: middah.name_english,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: MiddahUpdateForm) =>
      // Note: The API uses name_transliterated as the identifier
      // For now, we'll just show the form but note that the update endpoint doesn't exist
      // Based on the SDK, there's only create, get, and delete - no update/patch
      Promise.reject(new Error("Update endpoint not available")),
    onSuccess: () => {
      showSuccessToast("Middah updated successfully.")
      reset()
      setIsOpen(false)
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["middot"] })
    },
  })

  const onSubmit: SubmitHandler<MiddahUpdateForm> = async (data) => {
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
          View Middah
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>View Middah</DialogTitle>
        </DialogHeader>
        <DialogBody>
          <Text mb={4}>Middah details (editing not yet supported by API):</Text>
          <VStack gap={4} alignItems="flex-start">
            <Field label="Name (Transliterated)">
              <Input value={middah.name_transliterated} isReadOnly />
            </Field>

            <Field label="Name (Hebrew)">
              <Input value={middah.name_hebrew} isReadOnly />
            </Field>

            <Field label="Name (English)">
              <Input value={middah.name_english} isReadOnly />
            </Field>
          </VStack>
        </DialogBody>

        <DialogFooter gap={2}>
          <DialogActionTrigger asChild>
            <Button variant="subtle" colorPalette="gray">
              Close
            </Button>
          </DialogActionTrigger>
        </DialogFooter>
        <DialogCloseTrigger />
      </DialogContent>
    </DialogRoot>
  )
}

export default EditMiddah
