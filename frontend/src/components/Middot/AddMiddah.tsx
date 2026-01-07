import {
  Button,
  DialogActionTrigger,
  DialogTitle,
  Input,
  Text,
  VStack,
} from "@chakra-ui/react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useState } from "react"
import { type SubmitHandler, useForm } from "react-hook-form"
import { FaPlus } from "react-icons/fa"

import { type MiddahCreate, MiddotService } from "@/client"
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

const AddMiddah = () => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast } = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isValid, isSubmitting },
  } = useForm<MiddahCreate>({
    mode: "onTouched",
    criteriaMode: "all",
    defaultValues: {
      name_transliterated: "",
      name_hebrew: "",
      name_english: "",
    },
  })

  const mutation = useMutation({
    mutationFn: (data: MiddahCreate) =>
      MiddotService.createMiddah({ requestBody: data }),
    onSuccess: () => {
      showSuccessToast("Middah created successfully.")
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

  const onSubmit: SubmitHandler<MiddahCreate> = (data) => {
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
        <Button value="add-middah" my={4}>
          <FaPlus fontSize="16px" />
          Add Middah
        </Button>
      </DialogTrigger>
      <DialogContent>
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogHeader>
            <DialogTitle>Add Middah</DialogTitle>
          </DialogHeader>
          <DialogBody>
            <Text mb={4}>Fill in the details to add a new middah.</Text>
            <VStack gap={4}>
              <Field
                required
                invalid={!!errors.name_transliterated}
                errorText={errors.name_transliterated?.message}
                label="Name (Transliterated)"
              >
                <Input
                  {...register("name_transliterated", {
                    required: "Transliterated name is required.",
                  })}
                  placeholder="e.g., Chesed"
                  type="text"
                />
              </Field>

              <Field
                required
                invalid={!!errors.name_hebrew}
                errorText={errors.name_hebrew?.message}
                label="Name (Hebrew)"
              >
                <Input
                  {...register("name_hebrew", {
                    required: "Hebrew name is required.",
                  })}
                  placeholder="e.g., חסד"
                  type="text"
                />
              </Field>

              <Field
                required
                invalid={!!errors.name_english}
                errorText={errors.name_english?.message}
                label="Name (English)"
              >
                <Input
                  {...register("name_english", {
                    required: "English name is required.",
                  })}
                  placeholder="e.g., Kindness"
                  type="text"
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

export default AddMiddah
