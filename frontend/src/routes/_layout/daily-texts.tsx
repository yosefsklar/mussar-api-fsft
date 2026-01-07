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

import { DailyTextsService } from "@/client"
import { DailyTextActionsMenu } from "@/components/Common/DailyTextActionsMenu"
import AddDailyText from "@/components/DailyTexts/AddDailyText"

function getDailyTextsQueryOptions() {
  return {
    queryFn: () => DailyTextsService.listDailyTexts(),
    queryKey: ["dailyTexts"],
  }
}

export const Route = createFileRoute("/_layout/daily-texts")({
  component: DailyTexts,
})

function DailyTextsTable() {
  const { data, isLoading } = useQuery(getDailyTextsQueryOptions())

  const dailyTexts = data ?? []

  if (isLoading) {
    return (
      <Flex justify="center" align="center" h="200px">
        Loading...
      </Flex>
    )
  }

  if (dailyTexts.length === 0) {
    return (
      <EmptyState.Root>
        <EmptyState.Content>
          <EmptyState.Indicator>
            <FiSearch />
          </EmptyState.Indicator>
          <VStack textAlign="center">
            <EmptyState.Title>You don't have any daily texts yet</EmptyState.Title>
            <EmptyState.Description>
              Add a new daily text to get started
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
          <Table.ColumnHeader w="md">Title</Table.ColumnHeader>
          <Table.ColumnHeader>Text</Table.ColumnHeader>
          <Table.ColumnHeader w="sm">Actions</Table.ColumnHeader>
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {dailyTexts.map((dailyText) => (
          <Table.Row key={dailyText.id}>
            <Table.Cell truncate maxW="sm">
              {dailyText.id}
            </Table.Cell>
            <Table.Cell truncate maxW="sm">
              {dailyText.middah}
            </Table.Cell>
            <Table.Cell truncate maxW="md">
              {dailyText.title || "-"}
            </Table.Cell>
            <Table.Cell maxW="lg">
              {dailyText.sefaria_url ? (
                <a href={dailyText.sefaria_url} target="_blank" rel="noopener noreferrer" style={{ color: "blue", textDecoration: "underline" }}>
                  {dailyText.sefaria_url}
                </a>
              ) : null}
              {dailyText.content && (
                <div style={{ marginTop: dailyText.sefaria_url ? "4px" : "0" }}>
                  "{dailyText.content}"
                </div>
              )}
              {!dailyText.sefaria_url && !dailyText.content && "-"}
            </Table.Cell>
            <Table.Cell>
              <DailyTextActionsMenu dailyText={dailyText} />
            </Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table.Root>
  )
}

function DailyTexts() {
  return (
    <Container maxW="full">
      <Heading size="lg" pt={12}>
        Daily Texts Management
      </Heading>
      <AddDailyText />
      <DailyTextsTable />
    </Container>
  )
}

export default DailyTexts
