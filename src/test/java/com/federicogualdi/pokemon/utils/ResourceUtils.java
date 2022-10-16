package com.federicogualdi.pokemon.utils;

import org.apache.commons.io.IOUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.Objects;

public class ResourceUtils {
    private static final Logger logger = LoggerFactory.getLogger(ResourceUtils.class);

    public static String getResource(String path) {
        try (InputStream stream =
                     Thread.currentThread().getContextClassLoader().getResourceAsStream(path)) {
            if (Objects.nonNull(stream)) return IOUtils.toString(stream, StandardCharsets.UTF_8);
        } catch (Exception e) {
            logger.error("Error on db reset: {}", e.getMessage(), e);
        }

        return "";
    }
}
