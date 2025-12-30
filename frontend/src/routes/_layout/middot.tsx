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

import { MiddotService } from "@/client"
import { MiddahActionsMenu } from "@/components/Common/MiddahActionsMenu"
import AddMiddah from "@/components/Middot/AddMiddah"

function getMiddotQueryOptions() {
  return {
    queryFn: () => MiddotService.listMiddot(),
    queryKey: ["middot"],
  }
}

export const Route = createFileRoute("/_layout/middot")({
  component: Middot,
})

function MiddotTable() {
  const { data, isLoading } = useQuery(getMiddotQueryOptions())

  const middot = data ?? []

  if (isLoading) {
    return (
      <Flex justify="center" align="center" h="200px">
        Loading...
      </Flex>
    )
  }

  if (middot.length === 0) {
    return (
      <EmptyState.Root>
        <EmptyState.Content>
          <EmptyState.Indicator>
            <FiSearch />
          </EmptyState.Indicator>
          <VStack textAlign="center">
            <EmptyState.Title>You don't have any middot yet</EmptyState.Title>
            <EmptyState.Description>
              Add a new middah to get started
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
          <Table.ColumnHeader w="sm">Name (Transliterated)</Table.ColumnHeader>
          <Table.ColumnHeader w="sm">Name (Hebrew)</Table.ColumnHeader>
          <Table.ColumnHeader w="sm">Name (English)</Table.ColumnHeader>
          <Table.ColumnHeader w="sm">Actions</Table.ColumnHeader>
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {middot.map((middah) => (
          <Table.Row key={middah.name_transliterated}>
            <Table.Cell truncate maxW="sm">
              {middah.name_transliterated}
            </Table.Cell>
            <Table.Cell truncate maxW="sm">
              {middah.name_hebrew}
            </Table.Cell>
            <Table.Cell truncate maxW="sm">
              {middah.name_english}
            </Table.Cell>
            <Table.Cell>
              <MiddahActionsMenu middah={middah} />
            </Table.Cell>
          </Table.Row>
        ))}
      </Table.Body> 
    </Table.Root>
  )
}

function Middot() {
  return (
    <Container maxW="full">
      <Heading size="lg" pt={12}>
        Middot Management
      </Heading>
      <AddMiddah />
      <MiddotTable />
    </Container>
  )
}

