
<template>
  <div>
    <input type="file" @change="processFile">
    <div v-if="csvData">
      <h2>CSV Data:</h2>
      <table>
        <thead>
          <tr>
            <th v-for="(value, key) in csvData[0]" :key="key">{{ key }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(row, index) in csvData" :key="index">
            <td v-for="(value, key) in row" :key="key">{{ value }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="specificConductance">
      <h2>Specific Conductance:</h2>
      <table>
        <thead>
          <tr>
            <th>Index</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(value, index) in specificConductance" :key="index">
            <td>{{ index }}</td>
            <td>{{ value }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import Papa from 'papaparse'
import axios from 'axios'

function calculate_specific_conductance_seawater(AC, T, r = 0.19558593750000013) {
  return AC / (1 + r * (T - 25));
}

export default {
  data() {
    return {
      csvData: null,
      specificConductance: null
    }
  },
  methods: {
    processFile(event) {
      const file = event.target.files[0]
      Papa.parse(file, {
        header: true,
        complete: (results) => {
          const data = results.data
          const highRange = data.map(row => row['HighRange'])
          const temp = data.map(row => row['temp'])
          this.uploadData(highRange, temp)
          this.csvData = data.slice(8, 18)  // Display the first 10 rows of the CSV file
          this.specificConductance = highRange.map((ye, i) => calculate_specific_conductance_seawater(ye, temp[i]))
        }
      })
    },
    uploadData(highRange, temp) {
      axios.post('/api/upload', { highRange, temp })
        .then(() => console.log('Data uploaded successfully.'))
        .catch(err => console.error(err))
    }
  }
}
</script>