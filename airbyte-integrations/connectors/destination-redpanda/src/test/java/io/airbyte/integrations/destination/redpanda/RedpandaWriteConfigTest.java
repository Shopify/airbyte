package io.airbyte.integrations.destination.redpanda;

import static org.assertj.core.api.Assertions.assertThat;

import io.airbyte.protocol.models.DestinationSyncMode;
import org.junit.jupiter.api.Test;

class RedpandaWriteConfigTest {

    @Test
    void testRedpandaWriteConfig() {

        var writeConfig = new RedpandaWriteConfig("namespace_stream", DestinationSyncMode.OVERWRITE);

        assertThat(writeConfig)
            .hasFieldOrPropertyWithValue("topicName", "namespace_stream")
            .hasFieldOrPropertyWithValue("destinationSyncMode", DestinationSyncMode.OVERWRITE);

    }

}
