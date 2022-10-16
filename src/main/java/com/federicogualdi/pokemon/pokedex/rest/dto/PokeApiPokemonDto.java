package com.federicogualdi.pokemon.pokedex.rest.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.List;
import java.util.Objects;

public class PokeApiPokemonDto {
    public String name;
    @JsonProperty("flavor_text_entries")
    public List<PokeApiPokemonFlavorTextEntriesDto> flavorTextEntries;
    public PokeApiPokemonHabitatDto habitat;
    @JsonProperty("is_legendary")
    public Boolean isLegendary;

    public PokeApiPokemonDto() {
    }

    public String getHabitatName() {
        return Objects.nonNull(habitat) ? habitat.name : null;
    }

    @Override
    public String toString() {
        return "PokeApiPokemonDto{" + "name='" + name + '\'' + ", habitat=" + habitat + ", isLegendary=" + isLegendary + '}';
    }
}


