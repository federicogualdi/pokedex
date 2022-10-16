package com.federicogualdi.pokemon.pokedex.rest.dto;

public class ErrorDto {

    private final String title;
    private final Integer status;
    private final String detail;

    public String getTitle() {
        return title;
    }

    public Integer getStatus() {
        return status;
    }

    public String getDetail() {
        return detail;
    }

    public static class Builder {
        private String title;
        private Integer status;
        private String detail;

        public Builder() {
        }

        public Builder title(String value) {
            title = value;
            return this;
        }

        public Builder status(Integer value) {
            status = value;
            return this;
        }

        public Builder detail(String value) {
            detail = value;
            return this;
        }

        public ErrorDto build() {
            return new ErrorDto(this);
        }
    }

    private ErrorDto(Builder builder) {
        title = builder.title;
        status = builder.status;
        detail = builder.detail;
    }

    @Override
    public String toString() {
        return "ErrorDto{" + "title='" + title + '\'' + ", status=" + status + ", detail='" + detail + '\'' + '}';
    }
}
