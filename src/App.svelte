<script>
  import { Content } from "carbon-components-svelte/src/UIShell";
  import { Select, SelectItem } from "carbon-components-svelte/src/Select";
  import Header from "./components/Header.svelte";
  import Theme from "./components/Theme.svelte";
  import { Search } from "carbon-components-svelte/src/Search";
  import { PaginationNav } from "carbon-components-svelte/src/PaginationNav";
  import { InlineLoading } from "carbon-components-svelte/src/InlineLoading";
  import { DataTable } from "carbon-components-svelte/src/DataTable";
  import { Grid, Row, Column } from "carbon-components-svelte/src/Grid";
  let theme = "g10";
</script>

<style lang="scss" global>
  @import "carbon-components-svelte/css/all";
</style>

<Theme persist bind:theme>
  <Header />
  <Content style="background: none; padding: 1rem">
    <Search />
    <Grid>
      <Row>
        <Column style="outline: 0px solid var(--cds-interactive-04)">
          <InlineLoading status="active" description="Searching..." />
        </Column>
        <Column style="outline: 0px solid var(--cds-interactive-04)">
          <InlineLoading status="finished" description="Found" />
        </Column>
        <Column style="outline: 0px solid var(--cds-interactive-04)">
          <InlineLoading status="error" description="Not found" />
        </Column>
        <Column style="outline: 0px solid var(--cds-interactive-04)">
          <Select
            labelText="Choose theme"
            bind:selected={theme}
            style="margin-bottom: 1rem">
            <SelectItem value="white" text="White" />
            <SelectItem value="g10" text="Gray 10" />
            <SelectItem value="g90" text="Gray 90" />
            <SelectItem value="g100" text="Gray 100" />
          </Select>
        </Column>
      </Row>
    </Grid>
    <DataTable
      sortable
      title="Search Results"
      description="The following are results for your query."
      headers={[{ key: 'name', value: 'Name' }, { key: 'author', value: 'Author' }, { key: 'year', value: 'Year' }, { key: 'cost', value: 'Cost', display: (cost) => cost + ' €' }, { key: 'addDate', value: 'Add date', display: (date) => new Date(date).toLocaleString(), sort: (a, b) => (new Date(a) <= new Date(b) ? -1 : 1) }]}
      rows={[{ id: 'a', name: 'Book 3', author: 'Human', year: 3000, cost: 100, addDate: '2020-10-21' }, { id: 'b', name: 'Book 1', author: 'Human', year: 443, cost: 200, addDate: '2020-09-10' }, { id: 'c', name: 'Book 2', author: 'Human', year: 80, cost: 150, addDate: '2020-11-24' }, { id: 'd', name: 'Book 6', author: 'Human', year: 3000, cost: 250, addDate: '2020-12-01' }, { id: 'e', name: 'Book 4', author: 'Human', year: 443, cost: 550, addDate: '2021-03-21' }, { id: 'f', name: 'Book 5', author: 'Human', year: 80, cost: 400, addDate: '2020-11-14' }]} />
    <PaginationNav total={3} loop />
  </Content>
</Theme>
