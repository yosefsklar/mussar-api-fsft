import {
  Container,
  EmptyState,
  Flex,
  Heading,
  Table,
  VStack,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { FiSearch } from "react-icons/fi"

import { ReminderPhrasesService } from "@/client"
import { ReminderPhraseActionsMenu } from "@/components/Common/ReminderPhraseActionsMenu"
import AddReminderPhrase from "@/components/ReminderPhrases/AddReminderPhrase"

function getReminderPhrasesQueryOptions() {
  return {
    queryFn: () => ReminderPhrasesService.listReminderPhrases(),
    queryKey: ["reminderPhrases"],
  }
}

export const Route = createFileRoute("/_layout/reminder-phrases")({
  component: ReminderPhrases,
})

function ReminderPhrasesTable() {
  const { data, isLoading } = useQuery(getReminderPhrasesQueryOptions())

  const reminderPhrases = data ?? []

  if (isLoading) {
    return (
      <Flex justify="center" align="center" h="200px">
        Loading...
      </Flex>
    )
  }

  if (reminderPhrases.length === 0) {
    return (
      <EmptyState.Root>
        <EmptyState.Content>
          <EmptyState.Indicator>
            <FiSearch />
          </EmptyState.Indicator>
          <VStack textAlign="center">
            <EmptyState.Title>You don't have any reminder phrases yet</EmptyState.Title>
            <EmptyState.Description>
              Add a new reminder phrase to get started
            </EmptyState.Description>
          </VStack>
        </EmptyState.Content>
      </EmptyState.Root>
    )
  }

  return (
    <Table.Root size={{ base: "sm", md: "md" }}>
      <Table.Header>
        <Table.Row>
          <Table.ColumnHeader w="sm">ID</Table.ColumnHeader>
          <Table.ColumnHeader w="sm">Middah</Table.ColumnHeader>
          <Table.ColumnHeader>Text</Table.ColumnHeader>
          <Table.ColumnHeader w="sm">Actions</Table.ColumnHeader>
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {reminderPhrases.map((reminderPhrase) => (
          <Table.Row key={reminderPhrase.id}>
            <Table.Cell truncate maxW="sm">
              {reminderPhrase.id}
            </Table.Cell>
            <Table.Cell truncate maxW="sm">
              {reminderPhrase.middah}
            </Table.Cell>
            <Table.Cell truncate maxW="lg">
              {reminderPhrase.text}
            </Table.Cell>
            <Table.Cell>
              <ReminderPhraseActionsMenu reminderPhrase={reminderPhrase} />
            </Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table.Root>
  )
}

function ReminderPhrases() {
  return (
    <Container maxW="full">
      <Heading size="lg" pt={12}>
        Reminder Phrases Management
      </Heading>
      <AddReminderPhrase />
      <ReminderPhrasesTable />
    </Container>
  )
}

export default ReminderPhrases
