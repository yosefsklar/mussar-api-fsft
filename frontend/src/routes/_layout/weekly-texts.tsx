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

import { WeeklyTextsService } from "@/client"
import { WeeklyTextActionsMenu } from "@/components/Common/WeeklyTextActionsMenu"
import AddWeeklyText from "@/components/WeeklyTexts/AddWeeklyText"

function getWeeklyTextsQueryOptions() {
  return {
    queryFn: () => WeeklyTextsService.listWeeklyTexts(),
    queryKey: ["weeklyTexts"],
  }
}

export const Route = createFileRoute("/_layout/weekly-texts")({
  component: WeeklyTexts,
})

function WeeklyTextsTable() {
  const { data, isLoading } = useQuery(getWeeklyTextsQueryOptions())

  const weeklyTexts = data ?? []

  if (isLoading) {
    return (
      <Flex justify="center" align="center" h="200px">
        Loading...
      </Flex>
    )
  }

  if (weeklyTexts.length === 0) {
    return (
      <EmptyState.Root>
        <EmptyState.Content>
          <EmptyState.Indicator>
            <FiSearch />
          </EmptyState.Indicator>
          <VStack textAlign="center">
            <EmptyState.Title>You don't have any weekly texts yet</EmptyState.Title>
            <EmptyState.Description>
              Add a new weekly text to get started
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
          <Table.ColumnHeader w="md">Title</Table.ColumnHeader>
          <Table.ColumnHeader>Text</Table.ColumnHeader>
          <Table.ColumnHeader w="sm">Actions</Table.ColumnHeader>
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {weeklyTexts.map((weeklyText) => (
          <Table.Row key={weeklyText.id}>
            <Table.Cell truncate maxW="sm">
              {weeklyText.id}
            </Table.Cell>
            <Table.Cell truncate maxW="md">
              {weeklyText.title || "-"}
            </Table.Cell>
            <Table.Cell maxW="lg">
              {weeklyText.sefaria_url ? (
                <a href={weeklyText.sefaria_url} target="_blank" rel="noopener noreferrer" style={{ color: "blue", textDecoration: "underline" }}>
                  {weeklyText.sefaria_url}
                </a>
              ) : null}
              {weeklyText.content && (
                <div style={{ marginTop: weeklyText.sefaria_url ? "4px" : "0" }}>
                  "{weeklyText.content}"
                </div>
              )}
              {!weeklyText.sefaria_url && !weeklyText.content && "-"}
            </Table.Cell>
            <Table.Cell>
              <WeeklyTextActionsMenu weeklyText={weeklyText} />
            </Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table.Root>
  )
}

function WeeklyTexts() {
  return (
    <Container maxW="full">
      <Heading size="lg" pt={12}>
        Weekly Texts Management
      </Heading>
      <AddWeeklyText />
      <WeeklyTextsTable />
    </Container>
  )
}

export default WeeklyTexts
