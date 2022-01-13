package metrics

import (
	"encoding/json"
	"fmt"
	"strconv"
	"time"

	"github.com/mackerelio/go-osstat/cpu"
	"github.com/mackerelio/go-osstat/memory"
	"github.com/prometheus/client_golang/prometheus"
)

// Given an interface, convert it to float64
// Useful if converting a string to float
func MapToFloat(mapData interface{}) float64{
	floatData, err := strconv.ParseFloat((fmt.Sprintf("%.0f", mapData)),64)
	if err != nil{
		fmt.Print(err)
	}
	return floatData
}

// Gets the ongoing counter from the CPU and adds it to the data
func SystemCPUMetrics(metricName string, helpText string, item string)*prometheus.CounterVec{
	before, err := cpu.Get()
	var beforeCPUMap map[string]interface{}
	// Converts struct into json                                                                                            
    beforeData, _ := json.Marshal(before)                                                                                                                                                                                                                
	// Assigns struct data to map so it can be parsed like json
    json.Unmarshal(beforeData, &beforeCPUMap)
	if err != nil{
		fmt.Print(err)
	}
	time.Sleep(time.Duration(1) * time.Second)
	after, err := cpu.Get()
	var afterCPUMap map[string]interface{}
	// Converts struct into json                                                                                            
    afterData, _ := json.Marshal(after)                                                                                                                                                                                                                
	// Assigns struct data to map so it can be parsed like json
    json.Unmarshal(afterData, &afterCPUMap)
	if err != nil{
		fmt.Print(err)
	}
	total := float64(after.Total - before.Total)
	var cpuMetric = prometheus.NewCounterVec(
	prometheus.CounterOpts{
		Name: metricName,
		Help: helpText,
	},
	[]string{"path"},
	)
	stat := float64(MapToFloat(afterCPUMap[item]) - MapToFloat(beforeCPUMap[item])/total*100)
	cpuMetric.WithLabelValues(fmt.Sprintf("%.f", stat)).Inc()
	return  cpuMetric
}
// Given the metric name, helptext, and item, create the metric data for memory
// for promotheus 
func SystemMemoryMetric(metricName string, helpText string, item string) *prometheus.CounterVec{
	memory, err := memory.Get()
	// Creates a map interface for memory stats data
	var memoryMap map[string]interface{}
	// Converts struct into json                                                                                            
    data, _ := json.Marshal(memory)                                                                                                                                                                                                                
	// Assigns struct data to map so it can be parsed like json
    json.Unmarshal(data, &memoryMap) 
	if err != nil{
		fmt.Print(err)
	}
	var memoryMetric = prometheus.NewCounterVec(
	prometheus.CounterOpts{
		Name: metricName,
		Help: helpText,
	},
	[]string{"path"},
	)
	memoryMetric.WithLabelValues(fmt.Sprintf("%.0f", memoryMap[item])).Inc()
	return  memoryMetric
}